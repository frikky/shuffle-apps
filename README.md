# Shuffle Apps
This is a repository for apps to be used in [Shuffle](https://github.com/frikky/shuffle)

**PS:** These apps should be valid with WALKOFF, but the SDK is different, meaning you have to change the FIRST line in each Dockerfile (FROM frikky/shuffle:app_sdk).

## App Creation
App creation can be done with the Shuffle App Creator (exports as OpenAPI) or Python, which makes it possible to connect _literally_ any tool. Always prioritize using the App Creator when applicable.

![Shuffle-workflow-categories](https://github.com/frikky/shuffle-workflows/blob/master/images/categories_circle_dark.png)

### References
* [App Development Process](https://github.com/frikky/shuffle-docs/blob/master/handbook/engineering/app_development.md)
* [Python app documentation](https://shuffler.io/docs/app_creation)
* [Apps in progress](https://github.com/frikky/Shuffle-apps/projects/1)

### Categories
We have defined eight (8) "major" categories of tools that are necessary to any cybersecurity threat. Most security-related tools can fit into one of these eight.
1. [Communication](https://github.com/frikky/Shuffle-apps/issues/26) 		- Any way to chat; WhatsApp, SMS, Email etc.
2. [Case Management](https://github.com/frikky/Shuffle-apps/issues/22)	- The central hub for operation teams.
3. [SIEM](https://github.com/frikky/Shuffle-apps/issues/21)							- Search engine for logs in an enterprise. Used to find evil.
4. [Assets](https://github.com/frikky/Shuffle-apps/issues/25) 					- Discover endpoint information. Vulnerabilities, owners, departments etc.
5. [IAM](https://github.com/frikky/Shuffle-apps/issues/86)  						- Access Management. Active Directory, Google Workspaces, Single Sign-on etc.
6. [Intelligence](https://github.com/frikky/Shuffle-apps/issues/24) 		- Typically a vendor explaining what you should be looking for.
7. [Network](https://github.com/frikky/Shuffle-apps/issues/27)					- Anything BETWEEN your connected devices. Firewalls, WAF, Switches, Bluetooth...
8. [Eradication](https://github.com/frikky/Shuffle-apps/issues/23) 			- Control machines directly to eradicate evil. Hard and undefined (EDR & AV)

## OpenAPI
Apps in this repository are mostly manually made. Shuffle is striving for standardization and accessability, and our effort is focused on OpenAPI rather than manual work. With this in mind, most app creation that supports REST API's will be continued here.

[Shuffle OpenAPI](https://github.com/frikky/security-openapis)

## Support
* [Discord](https://discord.gg/B2CBzUm)
* [Twitter](https://twitter.com/shuffleio)
* [Email](mailto:frikky@shuffler.io)
* [Open issue](https://github.com/frikky/Shuffle/issues/new)
* [Shuffler.io](https://shuffler.io/contact)

## External contributions
[**App magicians**](https://github.com/frikky/shuffle-apps)
<a href="https://github.com/frikky/shuffle-apps/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=frikky/shuffle-apps" />
</a>

[**OpenAPI creators**](https://github.com/frikky/security-openapis)
<a href="https://github.com/frikky/shuffle-apps/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=frikky/security-openapis" />
</a>

# License
All apps, workflows and modular parts of Shuffle including our App SDK is under licensed under MIT, meaning you can freely use it anywhere in any way you want.

# Contributing
Contributing guidelines for outlined [here](https://github.com/frikky/Shuffle/blob/master/.github/CONTRIBUTING.md).
