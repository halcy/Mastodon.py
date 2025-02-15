Administration and moderation
=============================
.. py:module:: mastodon
    :no-index:
.. py:class: Mastodon

These functions allow you to perform moderation actions on users and generally
process reports using the API. To do this, you need access to the "admin:read" and/or
"admin:write" scopes or their more granular variants (both for the application and the
access token), as well as at least moderator access. Mastodon.py will not request these
by default, as that would be very dangerous.

BIG WARNING: TREAT ANY ACCESS TOKENS THAT HAVE ADMIN CREDENTIALS AS EXTREMELY, MASSIVELY
SENSITIVE DATA AND MAKE EXTRA SURE TO REVOKE THEM AFTER TESTING, NOT LET THEM SIT IN FILES
SOMEWHERE, TRACK WHICH ARE ACTIVE, ET CETERA. ANY EXPOSURE OF SUCH ACCESS TOKENS MEANS YOU
EXPOSE THE PERSONAL DATA OF ALL YOUR USERS TO WHOEVER HAS THESE TOKENS. TREAT THEM WITH
EXTREME CARE.

This is not to say that you should not treat access tokens from admin accounts that do not
have admin: scopes attached with a lot of care, but be extra careful with those that do.

Accounts
--------
.. automethod:: Mastodon.admin_accounts_v2
.. automethod:: Mastodon.admin_accounts
.. automethod:: Mastodon.admin_accounts_v1
.. automethod:: Mastodon.admin_account
.. automethod:: Mastodon.admin_account_enable
.. automethod:: Mastodon.admin_account_approve
.. automethod:: Mastodon.admin_account_reject
.. automethod:: Mastodon.admin_account_unsilence
.. automethod:: Mastodon.admin_account_unsuspend
.. automethod:: Mastodon.admin_account_moderate

Reports
-------
.. automethod:: Mastodon.admin_reports
.. automethod:: Mastodon.admin_report
.. automethod:: Mastodon.admin_report_assign
.. automethod:: Mastodon.admin_report_unassign
.. automethod:: Mastodon.admin_report_reopen
.. automethod:: Mastodon.admin_report_resolve

Federation
----------
.. automethod:: Mastodon.admin_domain_blocks
.. automethod:: Mastodon.admin_create_domain_block
.. automethod:: Mastodon.admin_update_domain_block
.. automethod:: Mastodon.admin_delete_domain_block

Moderation actions
------------------
.. automethod:: Mastodon.admin_measures
.. automethod:: Mastodon.admin_dimensions
.. automethod:: Mastodon.admin_retention

Canonical email blocks
----------------------
.. automethod:: Mastodon.admin_canonical_email_blocks
.. automethod:: Mastodon.admin_canonical_email_block
.. automethod:: Mastodon.admin_test_canonical_email_block
.. automethod:: Mastodon.admin_create_canonical_email_block
.. automethod:: Mastodon.admin_delete_canonical_email_block

Email domain blocks
-------------------
.. automethod:: Mastodon.admin_email_domain_blocks
.. automethod:: Mastodon.admin_email_domain_block
.. automethod:: Mastodon.admin_create_email_domain_block
.. automethod:: Mastodon.admin_delete_email_domain_block

IP blocks
---------
.. automethod:: Mastodon.admin_ip_blocks
.. automethod:: Mastodon.admin_ip_block
.. automethod:: Mastodon.admin_create_ip_block
.. automethod:: Mastodon.admin_update_ip_block
.. automethod:: Mastodon.admin_delete_ip_block

Trend management
----------------
.. automethod:: Mastodon.admin_trending_tags
.. automethod:: Mastodon.admin_trending_statuses
.. automethod:: Mastodon.admin_trending_links
.. automethod:: Mastodon.admin_approve_trending_link
.. automethod:: Mastodon.admin_reject_trending_link
.. automethod:: Mastodon.admin_approve_trending_status
.. automethod:: Mastodon.admin_reject_trending_status
.. automethod:: Mastodon.admin_approve_trending_tag
.. automethod:: Mastodon.admin_reject_trending_tag
