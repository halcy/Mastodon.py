import pytest

from mastodon.errors import MastodonNotFoundError
from mastodon.return_types import AnnualReportState, WrappedAnnualReports
from mastodon.types_base import EmptyResponse


@pytest.mark.vcr()
def test_annual_reports(api):
    reports = api.annual_reports()

    assert isinstance(reports, WrappedAnnualReports)
    assert isinstance(reports.annual_reports, list)
    assert isinstance(reports.accounts, list)
    assert isinstance(reports.statuses, list)

    if reports.annual_reports:
        report = api.annual_report(reports.annual_reports[0].year)
        assert isinstance(report, WrappedAnnualReports)
        assert report.annual_reports[0].year == reports.annual_reports[0].year
        api.annual_report_read(reports.annual_reports[0].year)
    else:
        with pytest.raises(MastodonNotFoundError):
            api.annual_report(1900)
        with pytest.raises(MastodonNotFoundError):
            api.annual_report_read(1900)


@pytest.mark.vcr()
def test_annual_report_state_and_generate(api):
    state = api.annual_report_state(1900)
    assert isinstance(state, AnnualReportState)
    assert state.state == 'ineligible'

    result = api.annual_report_generate(1900)
    assert isinstance(result, EmptyResponse)
