from typing import Optional, Any, Callable, Dict, Union
import  requests
from requests.auth import HTTPBasicAuth
from requests.sessions import session
import tenacity

from src.core.log.logging_mixin import  LoggingMixin

class BaseOperator(LoggingMixin):
    def __init__(
                self,
                method: str = 'POST',
                base_url: Optional[str] = None,
                api_prefix: Optional[str] = None,
                auth_type: Any = HTTPBasicAuth
                ) -> None:
        self.base_url = base_url
        self.api_prefix = api_prefix
        self.airflow_service_url = f"{self.base_url}{self.api_prefix}"
        self.method = method.upper()
        
        self._retry_obj: Callable[..., Any]
        self.auth_type: Any = auth_type
        
    def _get_endpoint(self, endpoint):
        url = None
        if self.base_url and not self.base_url.endswith('/') and endpoint and not endpoint.startswith('/'):
            url = self.base_url + '/' + endpoint
        else:
            url = (self.base_url or '') + (endpoint or '')
        return url
    def _get_session(self,  
                username: Optional[str] = 'admin',
                passwd: Optional[str] = 'admin',
                headers: Optional[Dict[Any, Any]] = None) -> requests.Session:
        session = requests.Session()
        
        if self.auth_type:
            self.auth_type(username,passwd)
        if headers:
            session.headers.update(headers)
        return session
        
    def execute(self,
                endpoint: Optional[str],
                method: Optional[str]= None,
                data: Optional[Union[Dict[str, Any], str]] = None,
                params: Optional[Union[Dict[str, Any], str]] = None,
                headers: Optional[Dict[str, Any]] = None,
                username: Optional[str] = 'admin',
                passwd: Optional[str] = 'admin',
                extra_options: Optional[Dict[str, Any]] = None,
                **request_kwargs: Any,
                ) -> Any:
        r"""
        Performs the request

        :param endpoint: the endpoint to be called i.e. resource/v1/query?
        :type endpoint: str
        :param data: payload to be uploaded or request parameters
        :type data: dict
        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        :param extra_options: additional options to be used when executing the request
            i.e. {'check_response': False} to avoid checking raising exceptions on non
            2XX or 3XX status codes
        :type extra_options: dict
        :param request_kwargs: Additional kwargs to pass when creating a request.
            For example, ``run(json=obj)`` is passed as ``requests.Request(json=obj)``
        """
        extra_options = extra_options or {}
        
        
        session = self._get_session(username,passwd,headers)
        
        if self.base_url and not self.base_url.endswith('/') and endpoint and not endpoint.startswith('/'):
            url = self.base_url + '/' + endpoint
        else:
            url = (self.base_url or '') + (endpoint or '')
        self.method = (method or self.method)
        if self.method == 'GET' and params:
            # GET uses params
            req = requests.Request(self.method, url, params=data, headers=headers, **request_kwargs)
        elif self.method == 'HEAD':
            # HEAD doesn't use params
            req = requests.Request(self.method, url, headers=headers, **request_kwargs)
        else:
            # Others use data
            print(f'{self.method},url:{url},headers:{headers},data:{data}')
            
            req = requests.Request(self.method, url, data=data, headers=headers, **request_kwargs)
        prepped_request = session.prepare_request(req)
        self.log.info("Sending '%s' to url: %s", self.method, url)
        return self.run_and_check(session, prepped_request, extra_options)
            
    def check_response(self, response: requests.Response) -> None:
        """
        Checks the status code and raise an  exception on non 2XX or 3XX
        status codes

        :param response: A requests response object
        :type response: requests.response
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.log.error("HTTP error: %s", response.reason)
            self.log.error(response.text)
            raise requests.exceptions.HTTPError
        
    def run_and_check(
        self,
        session: requests.Session,
        prepped_request: requests.PreparedRequest,
        extra_options: Dict[Any, Any],
    ) -> Any:
        """
        Grabs extra options like timeout and actually runs the request,
        checking for the result

        :param session: the session to be used to execute the request
        :type session: requests.Session
        :param prepped_request: the prepared request generated in run()
        :type prepped_request: session.prepare_request
        :param extra_options: additional options to be used when executing the request
            i.e. {'check_response': False} to avoid checking raising exceptions on non 2XX
            or 3XX status codes
        :type extra_options: dict
        """
        extra_options = extra_options or {}

        try:
            response = session.send(
                prepped_request,
                stream=extra_options.get("stream", False),
                verify=extra_options.get("verify", True),
                proxies=extra_options.get("proxies", {}),
                cert=extra_options.get("cert"),
                timeout=extra_options.get("timeout"),
                allow_redirects=extra_options.get("allow_redirects", True),
            )

            if extra_options.get('check_response', True):
                self.check_response(response)
            return response

        except requests.exceptions.ConnectionError as ex:
            self.log.warning('%s Tenacity will retry to execute the operation', ex)
            raise ex
        
    def run_with_advanced_retry(self, _retry_args: Dict[Any, Any], *args: Any, **kwargs: Any) -> Any:
        """
        Runs run() with a Tenacity decorator attached to it. This is useful for
        connectors which might be disturbed by intermittent issues and should not
        instantly fail.

        :param _retry_args: Arguments which define the retry behaviour.
            See Tenacity documentation at https://github.com/jd/tenacity
        :type _retry_args: dict


        .. code-block:: python

            hook = BaseOperator(base_url='',method='GET')
            retry_args = dict(
                 wait=tenacity.wait_exponential(),
                 stop=tenacity.stop_after_attempt(10),
                 retry=requests.exceptions.ConnectionError
             )
             hook.run_with_advanced_retry(
                     endpoint='v1/test',
                     _retry_args=retry_args
                 )

        """
        self._retry_obj = tenacity.Retrying(**_retry_args)

        return self._retry_obj(self.run, *args, **kwargs)