import { t } from '@/locales'

export const themeList = [
  {
    label: t('views.system.theme.default'),
    value: '#3370FF',
    loginBackground: 'default'
  },
  {
    label: t('views.system.theme.orange'),
    value: '#FF8800',
    loginBackground: 'orange'
  },
  {
    label: t('views.system.theme.green'),
    value: '#00B69D',
    loginBackground: 'green'
  },
  {
    label: t('views.system.theme.purple'),
    value: '#7F3BF5',
    loginBackground: 'purple'
  },
  {
    label: t('views.system.theme.red'),
    value: '#F01D94',
    loginBackground: 'red'
  }
]

export function getThemeImg(val: string) {
  return themeList.filter((v) => v.value === val)?.[0]?.loginBackground || 'default'
}

export const defaultSetting = {
  icon: '',
  loginLogo: '',
  loginImage: '',
  title: 'MaxKB',
  slogan: t('views.system.theme.defaultSlogan')
}

export const defaultPlatformSetting = {
  showUserManual: true,
  userManualUrl: t('layout.userManualUrl'),
  showForum: true,
  forumUrl: t('layout.forumUrl'),
  showProject: true,
  projectUrl: 'https://github.com/1Panel-dev/MaxKB'
}

// 新增：扩展主题配置接口
export interface EnhancedThemeConfig {
  // 基础配置
  theme: string
  icon: string
  loginLogo: string
  loginImage: string
  title: string
  slogan: string
  
  // 新增Logo配置
  headerLogo: string
  favicon: string
  
  // 新增配色方案
  colorScheme: {
    primary: string
    secondary: string
    accent: string
  }
  
  // 品牌元素配置
  brandElements: {
    showBrandName: boolean
    brandPosition: 'left' | 'center' | 'right'
    logoSize: 'small' | 'medium' | 'large'
  }
  
  // 高级配置
  customCSS: string
  enableDarkMode: boolean
  
  // 平台设置
  showUserManual: boolean
  userManualUrl: string
  showForum: boolean
  forumUrl: string
  showProject: boolean
  projectUrl: string
}

// 新增：默认增强配置
export const defaultEnhancedSetting: EnhancedThemeConfig = {
  ...defaultSetting,
  ...defaultPlatformSetting,
  theme: '#3370FF',
  headerLogo: '',
  favicon: '',
  colorScheme: {
    primary: '#3370FF',
    secondary: '#6B7280',
    accent: '#10B981'
  },
  brandElements: {
    showBrandName: true,
    brandPosition: 'left',
    logoSize: 'medium'
  },
  customCSS: '',
  enableDarkMode: false
}

// 新增：颜色处理工具函数
export function lighten(color: string, amount: number): string {
  const num = parseInt(color.slice(1), 16)
  const amt = Math.round(2.55 * amount * 100)
  const R = (num >> 16) + amt
  const G = (num >> 8 & 0x00FF) + amt
  const B = (num & 0x0000FF) + amt
  return '#' + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
    (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
    (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1)
}

export function darken(color: string, amount: number): string {
  const num = parseInt(color.slice(1), 16)
  const amt = Math.round(2.55 * amount * 100)
  const R = (num >> 16) - amt
  const G = (num >> 8 & 0x00FF) - amt
  const B = (num & 0x0000FF) - amt
  return '#' + (0x1000000 + (R > 255 ? 255 : R < 0 ? 0 : R) * 0x10000 +
    (G > 255 ? 255 : G < 0 ? 0 : G) * 0x100 +
    (B > 255 ? 255 : B < 0 ? 0 : B)).toString(16).slice(1)
}

// 新增：生成完整色板
export function generateColorPalette(primaryColor: string) {
  return {
    primary: primaryColor,
    light: lighten(primaryColor, 0.2),
    dark: darken(primaryColor, 0.2),
    rgba: hexToRgba(primaryColor, 0.1)
  }
}

// 新增：动态更新CSS变量
export function updateCSSVariables(config: EnhancedThemeConfig) {
  const root = document.documentElement
  const palette = generateColorPalette(config.colorScheme.primary)
  
  // 更新主色调变量
  root.style.setProperty('--el-color-primary', palette.primary)
  root.style.setProperty('--el-color-primary-light-3', palette.light)
  root.style.setProperty('--el-color-primary-dark-2', palette.dark)
  
  // 更新辅助色变量
  root.style.setProperty('--app-secondary-color', config.colorScheme.secondary)
  root.style.setProperty('--app-accent-color', config.colorScheme.accent)
  
  // 更新渐变色变量
  root.style.setProperty('--app-gradient-primary', 
    `linear-gradient(135deg, ${config.colorScheme.primary}, ${config.colorScheme.secondary})`)
}

// 新增：更新Favicon
export function updateFavicon(faviconUrl: string) {
  if (!faviconUrl) return
  
  const link = document.querySelector('link[rel="icon"]') as HTMLLinkElement || 
    document.createElement('link')
  link.rel = 'icon'
  link.href = faviconUrl
  
  if (!document.querySelector('link[rel="icon"]')) {
    document.head.appendChild(link)
  }
}

// 新增：更新页面标题和meta信息
export function updateMetaTags(config: EnhancedThemeConfig) {
  // 更新页面标题
  document.title = config.title || 'MaxKB'
  
  // 更新meta描述
  let metaDescription = document.querySelector('meta[name="description"]') as HTMLMetaElement
  if (!metaDescription) {
    metaDescription = document.createElement('meta')
    metaDescription.name = 'description'
    document.head.appendChild(metaDescription)
  }
  metaDescription.content = config.slogan || 'MaxKB - AI知识库助手'
}

export function hexToRgba(hex?: string, alpha?: number) {
  // 将16进制颜色值的两个字符一起转换成十进制
  if (!hex) {
    return ''
  } else {
    const r = parseInt(hex.slice(1, 3), 16)
    const g = parseInt(hex.slice(3, 5), 16)
    const b = parseInt(hex.slice(5, 7), 16)

    // 返回RGBA格式的字符串
    return `rgba(${r}, ${g}, ${b}, ${alpha})`
  }
}
