import { ElectronAPI } from '@electron-toolkit/preload'

declare global {
  interface Window {
    electron: ElectronAPI
    api: {
      windowControls: {minimize: Function, close: Function}
    }
  }
}
