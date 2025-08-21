---
title: 'Mastodon.py: A Python library for the Mastodon API'
tags:
  - Python
  - Social Web
  - ActivityPub
  - Mastodon
  - Federated Social Networks
  - API
authors:
  - name: Lorenz Diener
    orcid: 0000-0001-9370-9243
    affiliation: 1
  - name: Corentin Delcourt
    affiliation: 2
affiliations:
  - index: 1
    name: icosahedron.website, Germany
  - index: 2
    name: chitter.xyz, France
date: 21 August 2025
bibliography: paper.bib
---

# Summary

**Mastodon** [@mastodon] is a free-software microblogging social media server that allows users to post short form text and media as part of the decentralized, federated ActivityPub [@activitypub] network. **Mastodon.py** is a Python library that provides a user-friendly wrapper around the Mastodon REST and streaming APIs, enabling researchers, developers, and educators to build bots, data-collection tools, teaching examples, and full-featured clients for Mastodon and other servers that offer a Mastodon-compatible API, such as Akkoma [@akkoma2025akkoma], GoToSocial [@gotosocial2025gotosocial] and SNAC [@snac2025snac].

The library exposes all methods available to users of the Mastodon API while simplifying its use by handling all the implementation details required to effectively interact with it, such as authentication, pagination and dealing with rate limits. It also provides extensive documentation of methods and return values available directly as part of the library, making development easier.

# Statement of need

Studying or integrating with federated social networks often requires substantial boilerplate: OAuth flows, multipart uploads, pagination, backoff under rate limits, or just plain figuring out from the API documentation what information is available where and how to get it. For many Python users - particularly those in data science, human-computer interaction, computational social science, or digital humanities - this plumbing distracts from core research objectives.

**Mastodon.py** addresses this gap by providing a stable and straightforward Python implementation of the API that takes care of the details and allows its users to focus on their actual, higher level goals, instead of getting bogged down in the details of how to achieve them.

These features have made Mastodon.py a common choice both for building anything from a simple bot to full clients [@jmcbray2024brutaldon], prototyping new integrations and tools for the Mastodon ecosystem [@scidsg2024mastodonScheduler; @mozillaAI2025byota], as well as research data collection [@hidayat2025optimizing; @wang2024failed; @vravcevic2025more].

# Ethics statement

One common research use of Mastodon.py is the collection of (meta)data about different Mastodon instances, users and the shape of the network. We would like to use this space to remind researchers using the library to be mindful of issues around consent when performing such data collection in an environment where many users are highly privacy-conscious and dislike being talked about, rather than to [@wahner2024don].

# Acknowledgements

Mastodon.py contains many small, but important additions and fixes by more authors than would be practical to include in this papers author list. We would like to take this space to thank them for their work in making Mastodon.py better.

# References
