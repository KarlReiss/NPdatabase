class objectMapper {
  /**
   *
   * @param source 提供值的对象
   * @param target 需要被赋值的对象
   */
  map(source: any, target: any): any {
    if (source == null || target == null) return source
    for (const prop in source) {
      if (Object.prototype.hasOwnProperty.call(target, prop)) target[prop] = source[prop]
    }
    return target
  }
}
export default new objectMapper()
