export class EventsConfigs {
  /**
   * wsStorage 浏览器缓存
   */
  static eventBus = {
    searchTab: 'app.eventBus:searchTab'
  }
  /**
   * wsStorage 浏览器缓存
   */
  static wsStorage = {
    app: {
      layout: 'app.wsStorage.app:layout',
      isDark: 'app.wsStorage.app:isDark',
      currentSize: 'app.wsStorage.app:currentSize',
      theme: 'app.wsStorage.app:theme'
    },
    dict: {
      dict: 'app.wsStorage.dict:dict'
    },
    locales: {
      lang: 'app.wsStorage.locales:lang'
    },
    user: {
      platform: 'app.wsStorage.user:platform',
      userInfo: 'app.wsStorage.user:userInfo',
      userType: 'app.wsStorage.user:userType',
      token: 'app.wsStorage.user:token',
      abpConfig: 'app.wsStorage.user:abpConfig',
      orgItems: 'app.wsStorage.user:orgItems'
    }
  }
  /**
   * pinia 临时仓储库
   */
  static pinia = {
    app: 'app.pinia:app',
    dict: 'app.pinia:dict',
    locales: 'app.pinia:locales',
    lock: 'app.pinia:lock',
    permission: 'app.pinia:permission',
    tagsView: 'app.pinia:tagsView',
    user: 'app.pinia:user'
  }
}
