import re
from functools import partial
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen, build_opener
from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.django_test import DjangoTest


class HypercarServeNextTest(DjangoTest):

    def get_ticket(self, service: str, content: str, helper_msg: str) -> CheckResult:
        try:
            page = self.read_page(f'http://localhost:{self.port}/get_ticket/{service}')
            if content in page:
                return CheckResult.true()
            else:
                return CheckResult.false(
                    f'Expected to have {content} on /get_ticket/{service} page after\n'
                    f'{helper_msg}'
                )
        except URLError:
            return CheckResult.false(
                f'Cannot connect to the /get_ticket/{service} page.'
            )

    def check_menu(self, service: str, content: str, menu_content: str,
                   helper_msg: str) -> CheckResult:
        try:
            result = self.get_ticket(service, content, helper_msg)
            if not result.result:
                return result

            page = self.read_page(f'http://localhost:{self.port}/processing')
            if menu_content in page:
                return CheckResult.true()
            else:
                return CheckResult.false(
                    f'Expected to have {menu_content} on /processing page after\n'
                    f'{helper_msg}'
                )
        except URLError:
            return CheckResult.false(
                f'Cannot connect to the /processing page.'
            )

    def check_next(self, service: str, content: str, menu_content: str,
                   next_content: str, make_process: bool, helper_msg: str) -> CheckResult:
        try:
            result = self.check_menu(service, content, menu_content, helper_msg)
            if not result.result:
                return result

            if make_process:
                result = self.process_ticket()
                if not result.result:
                    return result

            page = self.read_page(f'http://localhost:{self.port}/next')

            if next_content in page:
                return CheckResult.true()
            else:
                return CheckResult.false(
                    f'Expected to have {next_content} on /next page after\n'
                    f'{helper_msg}'
                )
        except URLError:
            return CheckResult.false(
                f'Cannot connect to the /next page.'
            )

    def process_ticket(self):
        response = urlopen(f'http://localhost:{self.port}/processing')
        csrf_options = re.findall(
            b'<input[^>]+value="(?P<csrf>\w+)"[^>]*>', response.read()
        )
        if not csrf_options:
            return CheckResult.false(
                'Add csrf_token to your form'
            )
        set_cookie = response.headers.get('Set-Cookie')
        opener = build_opener()
        opener.addheaders.append(('Cookie', set_cookie))
        try:
            opener.open(
                f'http://localhost:{self.port}/processing',
                data=urlencode({'csrfmiddlewaretoken': csrf_options[0]}).encode()
            )
        except HTTPError:
            return CheckResult.false(
                'Cannot send POST request to /processsing page'
            )
        return CheckResult.true()

    def generate(self):
        helper_msg_1 = '\tClient #1 get ticket for inflating tires\n'
        helper_msg_2 = helper_msg_1 + '\tClient #2 get ticket for changing oil\n'
        helper_msg_3 = helper_msg_2 + '\tClient #3 get ticket for changing oil\n'
        helper_msg_3 += '\tOperator processed client\n'
        helper_msg_4 = helper_msg_3 + '\tClient #4 get ticket for inflating tires\n'
        helper_msg_4 += '\tOperator processed client\n'
        helper_msg_5 = helper_msg_4 + '\tClient #5 get ticket for diagnostic\n'
        helper_msg_5 += '\tOperator processed client\n'
        return [
            TestCase(attach=self.check_server),
            TestCase(attach=partial(
                self.check_next,
                'inflate_tires',
                'Please wait around 0 minutes',
                'Inflate tires queue: 1',
                'Waiting for the next client',
                False,
                helper_msg_1
            )),
            TestCase(attach=partial(
                self.check_next,
                'change_oil',
                'Please wait around 0 minutes',
                'Change oil queue: 1',
                'Waiting for the next client',
                False,
                helper_msg_2
            )),
            TestCase(attach=partial(
                self.check_next,
                'change_oil',
                'Please wait around 2 minutes',
                'Change oil queue: 2',
                'Next ticket #2',
                True,
                helper_msg_3
            )),
            TestCase(attach=partial(
                self.check_next,
                'inflate_tires',
                'Please wait around 7 minutes',
                'Inflate tires queue: 2',
                'Next ticket #3',
                True,
                helper_msg_4
            )),
            TestCase(attach=partial(
                self.check_next,
                'diagnostic',
                'Please wait around 10 minutes',
                'Get diagnostic queue: 1',
                'Next ticket #1',
                True,
                helper_msg_5
            )),
        ]

    def check(self, reply, attach):
        return attach()


if __name__ == '__main__':
    HypercarServeNextTest('hypercar.manage').run_tests()
