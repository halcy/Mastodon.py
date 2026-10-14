# annual_reports.py - annual report endpoints
from mastodon.internals import Mastodon as Internals
from mastodon.return_types import AnnualReportState, WrappedAnnualReports
from mastodon.types_base import EmptyResponse
from mastodon.utility import api_version


class Mastodon(Internals):
    @api_version("4.3.0", "4.3.0")
    def annual_reports(self) -> WrappedAnnualReports:
        """
        Retrieve all annual reports for the logged-in user.
        """
        return self.__api_request('GET', '/api/v1/annual_reports')

    @api_version("4.4.0", "4.4.0")
    def annual_report(self, year: int) -> WrappedAnnualReports:
        """
        Retrieve the annual report for `year`.
        """
        return self.__api_request('GET', f'/api/v1/annual_reports/{year}')

    @api_version("4.6.0", "4.6.0")
    def annual_report_state(self, year: int) -> AnnualReportState:
        """
        Retrieve the generation state for the annual report for `year`.

        The returned `state` is one of `available`, `generating`, `eligible`,
        or `ineligible`.
        """
        return self.__api_request('GET', f'/api/v1/annual_reports/{year}/state')

    @api_version("4.3.0", "4.3.0")
    def annual_report_read(self, year: int) -> None:
        """
        Mark the annual report for `year` as read.
        """
        self.__api_request('POST', f'/api/v1/annual_reports/{year}/read')

    @api_version("4.6.0", "4.6.0")
    def annual_report_generate(self, year: int) -> EmptyResponse:
        """
        Request generation of the annual report for `year`.

        The server returns immediately if the report is already generated or
        ineligible, and may attach asynchronous-refresh information while generating.
        """
        return self.__api_request('POST', f'/api/v1/annual_reports/{year}/generate')
