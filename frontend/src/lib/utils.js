import { css } from "emotion";

export function stylesListToClassNames(styles) {
  return Object.keys(styles).reduce((classNames, styleKey) => {
    classNames[styleKey] = css(styles[styleKey]);
    return classNames;
  }, {});
}
