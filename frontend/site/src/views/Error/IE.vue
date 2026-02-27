<template>
  <div class="page">
    <h1>是时候升级你的浏览器了</h1>
    <p
      >你正在使用旧版 Internet
      Explorer（IE11以下版本或使用该内核的浏览器）。这意味着在升级浏览器前，你将无法访问此网站。</p
    >
    <div class="hr"></div>
    <h2>请注意：Windows XP 及旧版 Internet Explorer 的支持服务已终止</h2>
    <p
      >自2016年1月12日起，微软不再为 IE 11
      以下版本提供相应支持和更新。没有关键的浏览器安全更新，您的电脑可能易受有害病毒、间谍软件和其他恶意软件的攻击，它们可以窃取或损害您的业务数据和信息。请参阅
      <a href="/end-ie.html">微软对旧版 Internet Explorer 的支持服务已终止的说明</a> 。</p
    >
    <div class="hr"></div>
    <h2>更先进的浏览器</h2>
    <p class="targetline"
      >推荐使用以下浏览器的最新版本。如果你的电脑已有以下浏览器的最新版本则直接使用该浏览器极速模式访问<b
        id="referrer"
      >
        <script>
          document.write(targetUrlHTML)
        </script> </b
      >即可。</p
    >
    <!-- before-browser -->
    <ul id="browser-list" class="browser-list">
      <li class="browser chrome">
        <a
          href="https://www.google.cn/chrome/thank-you.html?standalone=1&amp;statcb=0&amp;installdataindex=empty"
          id="browser-chrome-link"
          ><img src="/images/chrome.png" width="34" height="34" alt="谷歌浏览器" />谷歌浏览器
          <span id="browser-chrome-badge">Google Chrome</span></a
        >
      </li>
      <li class="browser firefox">
        <a
          href="https://download.mozilla.org/?product=firefox-latest-ssl&amp;os=win&amp;lang=zh-CN"
          id="browser-firefox-link"
          ><img src="/images/firefox.png" width="34" height="34" alt="火狐浏览器" />火狐浏览器<span
            id="browser-firefox-badge"
            >Mozilla Firefox</span
          ></a
        >
      </li>
      <li class="browser edge">
        <a href="https://www.microsoft.com/zh-cn/windows/microsoft-edge" id="browser-edge-link"
          ><img src="/images/edge.png" width="34" height="34" alt="微软浏览器" />微软浏览器<span
            id="browser-edge-badge"
            >Microsoft Edge</span
          ></a
        >
      </li>
      <li class="browser ie2345">
        <a
          href="https://dn-2345.cdn.bcebos.com/download/p8_k2345886_v2.0.exe"
          id="browser-ie2345-link"
          ><img
            src="/images/ie2345.png"
            width="34"
            height="34"
            alt="2345浏览器"
          />2345加速浏览器<span id="browser-ie2345-badge">双内核安全版</span></a
        >
      </li>
      <li class="browser se360">
        <a
          href="https://sfdl.360safe.com/netunion/20140425/360se+75526+n1abed0ce91.exe"
          id="browser-se360-link"
          ><img
            src="/images/se360.png"
            width="34"
            height="34"
            alt="360安全浏览器"
          />360安全浏览器<span id="browser-se360-badge">小白用户选择</span></a
        >
      </li>
      <li class="browser csex360">
        <a
          href="https://sfdl.360safe.com/netunion/20140425/360csex+75526+n1abed0ce91.exe"
          id="browser-csex360-link"
          ><img
            src="/images/csex360.png"
            width="34"
            height="34"
            alt="360极速浏览器X"
          />360极速浏览器X<span id="browser-csex360-badge">64位双核浏览器</span></a
        >
      </li>
      <li class="browser clearleft"></li>
    </ul>
    <!-- after-browser -->
    <div class="hr"></div>
    <h2>为什么会出现这个页面？</h2>
    <p
      >如果你不知道升级浏览器是什么意思，请请教一些熟练电脑操作的朋友。如果你使用的不是IE6/7/8/9/10，而是360浏览器、QQ浏览器、搜狗浏览器等，出现这个页面是因为你使用的不是该浏览器的最新版本，升级至最新即可。
    </p>
    <div class="hr"></div>
    <h2>一起抵制IE6、IE7、IE8、IE9、IE10</h2>
    <p
      >为了兼容这个曾经的浏览器霸主，网页设计人员需要做大量的代码工作。对于普通用户而言，低版本IE更是一个岌岌可危的安全隐患，在Windows历史上几次大的木马病毒事件都是利用IE漏洞进行传播。所以，请和我们一起抵制IE的过期版本！
    </p>
  </div>
</template>
<script>
// simple error report by baidu tongji

const er3eport = {}
er3eport.start = new Date().getTime()
er3eport.codetime = function () {
  return new Date().getTime() - er3eport.start
}
er3eport.dodnt = function () {
  window.dnt = 1
  if (typeof window.dodnt === 'function') window.dodnt()
}
er3eport.jqdefined = function () {
  er3eport.dodnt()
}
er3eport.listener = function (msg) {
  let logstr = false
  let errtype = 'JSERROR'
  if (typeof msg === 'string') {
    logstr = msg
  } else {
    if (msg.error) logstr = msg.error.stack
    else if (msg.message) logstr = msg.message

    let src
    if (msg.srcElement && msg.srcElement.src) src = msg.srcElement.src
    else if (msg.target && msg.target.src) src = msg.target.src

    if (!logstr) {
      if (src) {
        logstr = 'FileError: ' + src
        errtype = 'FILEERROR'
      } else if (msg.type) {
        logstr = msg.type
      }
    }
  }

  if (typeof logstr !== 'string') {
    logstr = 'empty_error_string'
  } else {
    logstr = logstr.replace(/\n/g, '').replace(/\s+/g, ' ')
  }

  return true
}
er3eport.ready = function () {
  if (document.readyState != 'complete') return
  const el = document.getElementsByTagName('A')
  let i
  for (i = 0; i < el.length; i++) {
    if (!!el[i].id && el[i].id.match(/^browser-/) !== null && !!el[i].href) {
      el[i].href = decodeURIComponent(el[i].href)
    }
  }
}

if (typeof jQuery === 'function') er3eport.jqdefined()
if (Object.defineProperty) Object.defineProperty(window, 'jQuery', { set: er3eport.jqdefined })

if (window.addEventListener) {
  window.addEventListener('error', er3eport.listener, true)
  document.addEventListener('readystatechange', er3eport.ready, true)
} else if (window.attachEvent) {
  window.attachEvent('onerror', er3eport.listener)
  document.attachEvent('onreadystatechange', er3eport.ready)
}

let l = window.location,
  s = l.search.substr(1),
  ra = 1,
  r = '',
  dr = document.referrer,
  r1 = s.match(/(^|&)referrer=((http|https)[^&]*)/),
  r2 = s.match(/^referrer=((http|https)\:\/\/.*)$/)
if (r2 !== null) r = r2[1]
else if (r1 !== null) r = r1[2]
if (
  r === '' &&
  dr !== '' &&
  ra === 1 &&
  dr.match(
    /\/(?:.*\.dmeng\.net|(?:(?:(?:www|m|wap|cn|search)\.)?(?:google|baidu|sogou|bing|so|yahoo|yandex|duckduckgo)\.com(?:\.[a-z]+)?))/
  ) === null
) {
  l.href =
    l.protocol + '//' + l.hostname + l.pathname + '?referrer=' + encodeURIComponent(dr) + '&' + s
}
let url = decodeURIComponent(r)
if (url.indexOf(window.location.hostname + '/') != -1) url = ''
let targetUrlHTML = ''
if (url !== '') {
  const m = url.match(/^(https?\:\/\/[^/]+\/)index\.html$/)
  targetUrlHTML =
    '&nbsp;<a href="' +
    url +
    '" onclick="alert(\'点击右键“复制快捷方式”（复制链接）到更先进的浏览器访问。\');return false;" rel="noreferrer">' +
    (m ? m[1] : url) +
    '</a>&nbsp;'
}
setTimeout(function () {
  let realPathname = window.location.pathname
  // ie 兼容
  if (realPathname.indexOf('/') !== 0) {
    realPathname = '/' + realPathname
  }
  window.dodnt = function () {
    const now = new Date()
    let time = now.getTime()
    time += 600 * 1000
    now.setTime(time)
    document.cookie = 'dnt=1' + '; expires=' + now.toUTCString() + '; path=/'
  }
  const doTrack = typeof window.dnt === 'undefined'
  if (doTrack === false && document.cookie.match(/dnt=1/) === null) window.dodnt()
}, 1500)
</script>
<style scoped>
/* Eric Meyer's Reset CSS v2.0 - http://cssreset.com */
html,
body,
div,
span,
applet,
object,
iframe,
h1,
h2,
h3,
h4,
h5,
h6,
p,
blockquote,
pre,
a,
abbr,
acronym,
address,
big,
cite,
code,
del,
dfn,
em,
img,
ins,
kbd,
q,
s,
samp,
small,
strike,
strong,
sub,
sup,
tt,
var,
b,
u,
i,
center,
dl,
dt,
dd,
ol,
ul,
li,
fieldset,
form,
label,
legend,
table,
caption,
tbody,
tfoot,
thead,
tr,
th,
td,
article,
aside,
canvas,
details,
embed,
figure,
figcaption,
footer,
header,
hgroup,
menu,
nav,
output,
ruby,
section,
summary,
time,
mark,
audio,
video {
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
  margin: 0;
  padding: 0;
}

article,
aside,
details,
figcaption,
figure,
footer,
header,
hgroup,
menu,
nav,
section {
  display: block;
}

body {
  line-height: 1;
}

ol,
ul {
  list-style: none;
}

blockquote,
q {
  quotes: none;
}

blockquote:before,
blockquote:after,
q:before,
q:after {
  content: none;
}

table {
  border-collapse: collapse;
  border-spacing: 0;
}

*,
::after,
::before {
  box-sizing: border-box;
}

a {
  text-decoration: none;
  color: #0072c6;
}

a:hover {
  text-decoration: none;
  color: #004d8c;
}

body {
  text-align: center;
  font-size: 14px;
  line-height: 24px;
  font-family:
    Microsoft YaHei,
    '瀹嬩綋',
    sans-serif;
  color: #454545;
  overflow-y: scroll;
  _overflow-y: auto;
  *overflow-y: auto;
}

.page {
  width: 960px;
  margin: 0 auto;
  padding: 10px;
  text-align: left;
}

h2,
h3 {
  font-family: Microsoft YaHei;
}

h1 {
  font-size: 40px;
  line-height: 60px;
  font-weight: 100;
  margin: 20px 0 15px;
}

h2 {
  font-size: 20px;
  line-height: 25px;
  font-weight: 100;
  margin: 10px 0;
}

h3 {
  font-weight: bold;
}

code {
  padding: 2px 4px;
  font-size: 95%;
  color: #c7254e;
  background-color: #f9f2f4;
  border-radius: 4px;
}

pre code {
  white-space: pre-wrap;
  word-break: break-word;
  display: inline-block;
  word-break: break-all;
}

ul {
  padding: 0 1em;
}

ul li {
  list-style-type: disc;
  list-style-position: inside;
}

b,
strong {
  font-weight: bold;
}

em {
  color: red;
}

p {
  margin-bottom: 10px;
}

hr,
.hr {
  margin: 20px 0;
  border: 0;
  width: 100%;
  height: 1px;
  overflow: hidden;
  background-color: #ccc;
}

.text-right {
  text-align: right;
}

.clearboth {
  clear: both;
  width: 100%;
  content: '';
}

.clearleft {
  clear: left;
  width: 100%;
  content: '';
}

.clearright {
  clear: right;
  width: 100%;
  content: '';
}

.browser-list {
  margin: 16px 0 10px;
  padding: 0;
  height: 42px;
  _overflow: hidden;
}

.browser {
  display: block;
  width: 155px;
  height: 34px;
  line-height: 22px;
  float: left;
  list-style: none;
}

.browser.clearleft {
  height: 1px;
}

.browser span {
  display: block;
  font-size: 12px;
  line-height: 1.2;
}

.browser img {
  width: 34px;
  height: 34px;
  border: 0;
  float: left;
  margin-right: 10px;
}

.browser.firefox {
  width: 150px;
}

.browser.edge {
  width: 150px;
}

.browser.ie2345 {
  width: 170px;
}

.browser.se360 {
  width: 160px;
}

.browser.qqbrowser {
  width: 140px;
}

.small-alert {
  font-size: 12px;
  margin: 15px 0 8px;
  color: #90949c;
}

.small-alert:not(.hide) + hr {
  margin-top: 0;
}

.hide {
  display: none;
}

.alert-danger {
  display: block;
  color: #777;
  background-color: #f1f1f1;
  padding: 6px 12px;
  _padding: 8px 12px 6px;
  clear: both;
}

.alert-info {
  color: #000;
  background-color: #f1f6fc;
  margin-top: 12px;
}

.alert-info img {
  vertical-align: text-top;
}

#win-danger {
  margin-top: 12px;
  position: relative;
}

#win-danger .arrow {
  background: url(/images/arrow.png) no-repeat;
  border: 0;
  position: absolute;
  display: block;
  width: 20px;
  height: 12px;
  left: 325px;
  top: -12px;
}

.targetline,
#referrer a {
  word-break: break-all;
}

.top-alert {
  background: #f2f2f2;
}

.top-alert-content {
  font-size: 14px;
}

@media only screen and (max-width: 959px) {
  .page {
    max-width: 100%;
    padding: 20px;
    font-size: 16px;
    line-height: 26px;
  }

  h1 {
    font-size: 26px;
    line-height: 1.8;
    font-weight: bold;
    margin-top: 0;
  }

  .browser-list {
    height: auto;
  }

  .browser {
    margin: 0 20px 20px 0;
  }

  code {
    word-break: break-word;
  }
}
</style>
