Return values
=============
.. py:module:: mastodon
   :no-index:
.. py:class: Mastodon

Unless otherwise specified, all data is returned as Python dictionaries, matching
the JSON format used by the API. Dates returned by the API are in ISO 8601 format
and are parsed into Python datetime objects.

To make access easier, the dictionaries returned are wrapped by a class that adds
read-only attributes for all dict values - this means that, for example, instead of
writing

.. code-block:: python

    description = mastodon.account_verify_credentials()["source"]["note"]

you can also just write

.. code-block:: python

    description = mastodon.account_verify_credentials().source.note

and everything will work as intended. The class used for this is exposed as
`AttribAccessDict`.

Since version 2.0.0, Mastodon.py is fully typed - there are now classes for all
return types, and all functions have type hints. Note that the base class is still
the AttribAccessDict - this means that you can still access all returned values as 
attributes, `even if a type does not define them`. Lists have been split into lists
that can be paginated (i.e. that have pagination attributes) and those that cannot.

All return values can be converted from and to JSON using the `to_json()` and `from_json()`
methods defined on the `mastodon.types_base.Entity` class.

Base types
==========
.. autoclass:: mastodon.types_base.AttribAccessDict
   :members:

.. autoclass:: mastodon.types_base.PaginatableList
   :members:

.. autoclass:: mastodon.types_base.NonPaginatableList
   :members:

.. autoclass:: mastodon.types_base.MaybeSnowflakeIdType
   :members:

.. autoclass:: mastodon.types_base.IdType
   :members:

.. autoclass:: mastodon.types_base.Entity
   :members:

.. autoclass:: mastodon.types_base.EntityList
   :members:

Return types
============
.. autoclass:: mastodon.return_types.Account
   :members:

.. autoclass:: mastodon.return_types.AccountField
   :members:

.. autoclass:: mastodon.return_types.Role
   :members:

.. autoclass:: mastodon.return_types.CredentialAccountSource
   :members:

.. autoclass:: mastodon.return_types.Status
   :members:

.. autoclass:: mastodon.return_types.Quote
   :members:

.. autoclass:: mastodon.return_types.ShallowQuote
   :members:

.. autoclass:: mastodon.return_types.StatusEdit
   :members:

.. autoclass:: mastodon.return_types.FilterResult
   :members:

.. autoclass:: mastodon.return_types.StatusMention
   :members:

.. autoclass:: mastodon.return_types.ScheduledStatus
   :members:

.. autoclass:: mastodon.return_types.ScheduledStatusParams
   :members:

.. autoclass:: mastodon.return_types.Poll
   :members:

.. autoclass:: mastodon.return_types.PollOption
   :members:

.. autoclass:: mastodon.return_types.Conversation
   :members:

.. autoclass:: mastodon.return_types.Tag
   :members:

.. autoclass:: mastodon.return_types.TagHistory
   :members:

.. autoclass:: mastodon.return_types.CustomEmoji
   :members:

.. autoclass:: mastodon.return_types.Application
   :members:

.. autoclass:: mastodon.return_types.Relationship
   :members:

.. autoclass:: mastodon.return_types.FilterV2
   :members:

.. autoclass:: mastodon.return_types.Notification
   :members:

.. autoclass:: mastodon.return_types.Context
   :members:

.. autoclass:: mastodon.return_types.UserList
   :members:

.. autoclass:: mastodon.return_types.MediaAttachment
   :members:

.. autoclass:: mastodon.return_types.MediaAttachmentMetadataContainer
   :members:

.. autoclass:: mastodon.return_types.MediaAttachmentImageMetadata
   :members:

.. autoclass:: mastodon.return_types.MediaAttachmentVideoMetadata
   :members:

.. autoclass:: mastodon.return_types.MediaAttachmentAudioMetadata
   :members:

.. autoclass:: mastodon.return_types.MediaAttachmentFocusPoint
   :members:

.. autoclass:: mastodon.return_types.MediaAttachmentColors
   :members:

.. autoclass:: mastodon.return_types.PreviewCard
   :members:

.. autoclass:: mastodon.return_types.TrendingLinkHistory
   :members:

.. autoclass:: mastodon.return_types.PreviewCardAuthor
   :members:

.. autoclass:: mastodon.return_types.SearchV2
   :members:

.. autoclass:: mastodon.return_types.Instance
   :members:

.. autoclass:: mastodon.return_types.InstanceConfiguration
   :members:

.. autoclass:: mastodon.return_types.InstanceURLs
   :members:

.. autoclass:: mastodon.return_types.InstanceV2
   :members:

.. autoclass:: mastodon.return_types.InstanceIcon
   :members:

.. autoclass:: mastodon.return_types.InstanceConfigurationV2
   :members:

.. autoclass:: mastodon.return_types.InstanceVapidKey
   :members:

.. autoclass:: mastodon.return_types.InstanceURLsV2
   :members:

.. autoclass:: mastodon.return_types.InstanceThumbnail
   :members:

.. autoclass:: mastodon.return_types.InstanceThumbnailVersions
   :members:

.. autoclass:: mastodon.return_types.InstanceStatistics
   :members:

.. autoclass:: mastodon.return_types.InstanceUsage
   :members:

.. autoclass:: mastodon.return_types.InstanceUsageUsers
   :members:

.. autoclass:: mastodon.return_types.RuleTranslation
   :members:

.. autoclass:: mastodon.return_types.Rule
   :members:

.. autoclass:: mastodon.return_types.InstanceRegistrations
   :members:

.. autoclass:: mastodon.return_types.InstanceContact
   :members:

.. autoclass:: mastodon.return_types.InstanceAccountConfiguration
   :members:

.. autoclass:: mastodon.return_types.InstanceStatusConfiguration
   :members:

.. autoclass:: mastodon.return_types.InstanceTranslationConfiguration
   :members:

.. autoclass:: mastodon.return_types.InstanceMediaConfiguration
   :members:

.. autoclass:: mastodon.return_types.InstancePollConfiguration
   :members:

.. autoclass:: mastodon.return_types.Nodeinfo
   :members:

.. autoclass:: mastodon.return_types.NodeinfoSoftware
   :members:

.. autoclass:: mastodon.return_types.NodeinfoServices
   :members:

.. autoclass:: mastodon.return_types.NodeinfoUsage
   :members:

.. autoclass:: mastodon.return_types.NodeinfoUsageUsers
   :members:

.. autoclass:: mastodon.return_types.NodeinfoMetadata
   :members:

.. autoclass:: mastodon.return_types.Activity
   :members:

.. autoclass:: mastodon.return_types.Report
   :members:

.. autoclass:: mastodon.return_types.AdminReport
   :members:

.. autoclass:: mastodon.return_types.WebPushSubscription
   :members:

.. autoclass:: mastodon.return_types.WebPushSubscriptionAlerts
   :members:

.. autoclass:: mastodon.return_types.PushNotification
   :members:

.. autoclass:: mastodon.return_types.Preferences
   :members:

.. autoclass:: mastodon.return_types.FeaturedTag
   :members:

.. autoclass:: mastodon.return_types.Marker
   :members:

.. autoclass:: mastodon.return_types.Announcement
   :members:

.. autoclass:: mastodon.return_types.Reaction
   :members:

.. autoclass:: mastodon.return_types.StreamReaction
   :members:

.. autoclass:: mastodon.return_types.FamiliarFollowers
   :members:

.. autoclass:: mastodon.return_types.AdminAccount
   :members:

.. autoclass:: mastodon.return_types.AdminIp
   :members:

.. autoclass:: mastodon.return_types.AdminMeasure
   :members:

.. autoclass:: mastodon.return_types.AdminMeasureData
   :members:

.. autoclass:: mastodon.return_types.AdminDimension
   :members:

.. autoclass:: mastodon.return_types.AdminDimensionData
   :members:

.. autoclass:: mastodon.return_types.AdminRetention
   :members:

.. autoclass:: mastodon.return_types.AdminCohort
   :members:

.. autoclass:: mastodon.return_types.AdminDomainBlock
   :members:

.. autoclass:: mastodon.return_types.AdminCanonicalEmailBlock
   :members:

.. autoclass:: mastodon.return_types.AdminDomainAllow
   :members:

.. autoclass:: mastodon.return_types.AdminEmailDomainBlock
   :members:

.. autoclass:: mastodon.return_types.AdminEmailDomainBlockHistory
   :members:

.. autoclass:: mastodon.return_types.AdminIpBlock
   :members:

.. autoclass:: mastodon.return_types.DomainBlock
   :members:

.. autoclass:: mastodon.return_types.ExtendedDescription
   :members:

.. autoclass:: mastodon.return_types.FilterKeyword
   :members:

.. autoclass:: mastodon.return_types.FilterStatus
   :members:

.. autoclass:: mastodon.return_types.StatusSource
   :members:

.. autoclass:: mastodon.return_types.Suggestion
   :members:

.. autoclass:: mastodon.return_types.Translation
   :members:

.. autoclass:: mastodon.return_types.AccountCreationError
   :members:

.. autoclass:: mastodon.return_types.AccountCreationErrorDetails
   :members:

.. autoclass:: mastodon.return_types.AccountCreationErrorDetailsField
   :members:

.. autoclass:: mastodon.return_types.NotificationPolicy
   :members:

.. autoclass:: mastodon.return_types.NotificationPolicySummary
   :members:

.. autoclass:: mastodon.return_types.RelationshipSeveranceEvent
   :members:

.. autoclass:: mastodon.return_types.GroupedNotificationsResults
   :members:

.. autoclass:: mastodon.return_types.PartialAccountWithAvatar
   :members:

.. autoclass:: mastodon.return_types.NotificationGroup
   :members:

.. autoclass:: mastodon.return_types.AccountWarning
   :members:

.. autoclass:: mastodon.return_types.UnreadNotificationsCount
   :members:

.. autoclass:: mastodon.return_types.Appeal
   :members:

.. autoclass:: mastodon.return_types.NotificationRequest
   :members:

.. autoclass:: mastodon.return_types.SupportedLocale
   :members:

.. autoclass:: mastodon.return_types.OAuthServerInfo
   :members:

.. autoclass:: mastodon.return_types.OAuthUserInfo
   :members:

.. autoclass:: mastodon.return_types.TermsOfService
   :members:

Deprecated types
================
.. autoclass:: mastodon.return_types.Filter
   :members:

.. autoclass:: mastodon.return_types.Search
   :members:

.. autoclass:: mastodon.return_types.IdentityProof
   :members:


