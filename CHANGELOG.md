# Changelog

## [3.1.4](https://github.com/dedsxc/xbot/compare/xbot-3.1.3...xbot-3.1.4) (2025-10-21)


### ⚠ BREAKING CHANGES

* use config.ini to configure the app. Rename the project to xBot

### Features

* add http server for healthcheck ([#80](https://github.com/dedsxc/xbot/issues/80)) ([e066b7f](https://github.com/dedsxc/xbot/commit/e066b7f55e45a2ee9e6d4af97a2d89eaf0742f87))
* allow fetching from multiple subreddit ([#92](https://github.com/dedsxc/xbot/issues/92)) ([d18002f](https://github.com/dedsxc/xbot/commit/d18002f8563882106ee3cdd9f11ec50ad587edde))
* blacklist reddit user ([#99](https://github.com/dedsxc/xbot/issues/99)) ([b4e9020](https://github.com/dedsxc/xbot/commit/b4e90203a5a0a6572b4c30d6a543b9f9fe6f6077))
* customize tweet ([#83](https://github.com/dedsxc/xbot/issues/83)) ([b511429](https://github.com/dedsxc/xbot/commit/b511429f41927d1ba050a34ee00c11af44d0e7ef))
* integrate ollama api ([#95](https://github.com/dedsxc/xbot/issues/95)) ([77466d7](https://github.com/dedsxc/xbot/commit/77466d7cd7cf26cfeacd0cfe42292baa566b0bde))
* separate bot service and use config.ini ([#79](https://github.com/dedsxc/xbot/issues/79)) ([fa0021a](https://github.com/dedsxc/xbot/commit/fa0021a412b8a6ec40d6870d452fc01a6340beab))
* upload galery image from reddit ([#73](https://github.com/dedsxc/xbot/issues/73)) ([56edc99](https://github.com/dedsxc/xbot/commit/56edc993c8fde20cfbe49cbd9b874a3214ab69db))
* use fastAPI and add buymeacoffee webhook ([#91](https://github.com/dedsxc/xbot/issues/91)) ([65fb753](https://github.com/dedsxc/xbot/commit/65fb753e064c2bb692d686a5c4ef9e57785d662b))


### Bug Fixes

* close selenium page to avoid ram consumption ([#75](https://github.com/dedsxc/xbot/issues/75)) ([b71b85f](https://github.com/dedsxc/xbot/commit/b71b85f56cf3b73ecaaa6ef795e999cb2aad8f86))
* improve redis error handling ([#85](https://github.com/dedsxc/xbot/issues/85)) ([a336c84](https://github.com/dedsxc/xbot/commit/a336c84d6e272a9a8433d8ce835d1578c206f4a4))
* manage flair better from config ([#84](https://github.com/dedsxc/xbot/issues/84)) ([b78e312](https://github.com/dedsxc/xbot/commit/b78e31262cc67a6a60f27f33923ecc3574430870))
* only download 4 img max ([#82](https://github.com/dedsxc/xbot/issues/82)) ([6901083](https://github.com/dedsxc/xbot/commit/6901083735103d3be47929f24276b0854efe5286))
* oops ([d35707c](https://github.com/dedsxc/xbot/commit/d35707c7f49a1910d4c59b87e3d2c1c5c2b90c48))
* oops 2 ([ada8aea](https://github.com/dedsxc/xbot/commit/ada8aead112a2ade6432d37f8a6d0c53f6fe6934))
* remove comment and suppress http log ([#81](https://github.com/dedsxc/xbot/issues/81)) ([d4c434c](https://github.com/dedsxc/xbot/commit/d4c434c9d710b5abf5b991c12bf959009a7b356f))
* reorg folder and add auto release ([#118](https://github.com/dedsxc/xbot/issues/118)) ([6327220](https://github.com/dedsxc/xbot/commit/6327220731f022ef4710c690c4a43b8ffab4bf4d))
* revert lemmy api ([#98](https://github.com/dedsxc/xbot/issues/98)) ([fdbd031](https://github.com/dedsxc/xbot/commit/fdbd0316c7cf59810c3eb72421fdc1832539dc8e))
* use cookie to connect on x.com ([#117](https://github.com/dedsxc/xbot/issues/117)) ([945bf7a](https://github.com/dedsxc/xbot/commit/945bf7a1462e18b4119dfcef77c32fabb75a0da4))
* use tini to kill zombie process ([#76](https://github.com/dedsxc/xbot/issues/76)) ([8a2af1e](https://github.com/dedsxc/xbot/commit/8a2af1e39adfedc93d51018c4e6e0c9fae793390))
* wait until media can be uploaded before posting it ([#72](https://github.com/dedsxc/xbot/issues/72)) ([5f2ecd6](https://github.com/dedsxc/xbot/commit/5f2ecd6d44d84e79923c0584aa6750f321d3a085))
