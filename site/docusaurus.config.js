import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI From Tensors to Agents on Mac Silicon',
  tagline: 'Learning modern AI by building it on Apple Silicon',
  url: 'https://hassanvfx.github.io',
  baseUrl: '/mac-ai/',
  organizationName: 'hassanvfx',
  projectName: 'mac-ai',
  onBrokenLinks: 'throw',
  presets: [[
    'classic',
    {
      docs: {path: '../book/chapters', routeBasePath: 'course', sidebarPath: './sidebars.js'},
      blog: false,
      theme: {customCss: './src/css/custom.css'}
    }
  ]],
  themeConfig: {
    navbar: {
      title: 'AI From Tensors to Agents',
      items: [
        {to: '/', label: 'Start here', position: 'left'},
        {to: '/course/', label: 'Course', position: 'left'},
        {to: '/labs/', label: 'Labs', position: 'left'},
        {href: 'https://github.com/hassanvfx/mac-ai', label: 'GitHub', position: 'right'}
      ]
    },
    footer: {
      style: 'dark',
      links: [],
      copyright: 'Copyright © ' + new Date().getFullYear() + ' Hassan Uriostegui · Waken AI Labs. Book content is all rights reserved.'
    },
    prism: {theme: prismThemes.github, darkTheme: prismThemes.dracula}
  }
};
export default config;
