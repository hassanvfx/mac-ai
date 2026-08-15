import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI From Tensors to Agents on Mac Silicon',
  tagline: 'Learning modern AI by building it on Apple Silicon',
  url: 'https://YOUR_GITHUB_USERNAME.github.io',
  baseUrl: '/from-tensors-to-agents/',
  organizationName: 'YOUR_GITHUB_USERNAME',
  projectName: 'from-tensors-to-agents',
  onBrokenLinks: 'throw',
  presets: [[
    'classic',
    {
      docs: {path: '../book/chapters', routeBasePath: '/', sidebarPath: './sidebars.js'},
      blog: false,
      theme: {customCss: './src/css/custom.css'}
    }
  ]],
  themeConfig: {
    navbar: {
      title: 'AI From Tensors to Agents',
      items: [
        {to: '/', label: 'Course', position: 'left'},
        {href: 'https://github.com/YOUR_GITHUB_USERNAME/from-tensors-to-agents', label: 'GitHub', position: 'right'}
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
