import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const site = path.resolve(here, '..');
const root = path.resolve(site, '..');
const generated = path.join(site, 'src', 'generated');
const labs = path.join(site, 'src', 'pages', 'labs');
const readme = fs.readFileSync(path.join(root, 'README.md'), 'utf8').replace(/^# .*\n/, '');
const manifest = JSON.parse(fs.readFileSync(path.join(site, 'reader-manifest.json'), 'utf8'));
const chapterSlugs = new Map(
  fs.readdirSync(path.join(root, 'book', 'chapters'))
    .filter((name) => name.endsWith('.md'))
    .map((name) => [name.slice(0, 2), name.replace(/^\d+-/, '').replace(/\.md$/, '')]),
);
fs.mkdirSync(generated, {recursive: true});
fs.mkdirSync(labs, {recursive: true});
fs.writeFileSync(path.join(generated, 'reader-onboarding.mdx'), readme);
fs.writeFileSync(path.join(labs, 'index.mdx'), `---\ntitle: Runnable labs\n---\n\n# Runnable labs\n\nRead the chapter, run one small experiment, inspect its benchmark record, then make one controlled change.\n\n${manifest.map((lab) => `- [Chapter ${lab.id}: ${lab.title}](./${lab.id})`).join('\n')}\n`);
for (const lab of manifest) {
  const github = `https://github.com/hassanvfx/mac-ai/blob/main/${lab.experiment}`;
  const slug = chapterSlugs.get(lab.id);
  fs.writeFileSync(path.join(labs, `${lab.id}.mdx`), `---\ntitle: Chapter ${lab.id} lab\n---\n\n# Chapter ${lab.id}: ${lab.title}\n\n## Run this lab on your Mac\n\n\`\`\`bash\n${lab.command}\n\`\`\`\n\n**Expected:** ${lab.expected}\n\n- [Open the experiment source](${github})\n- [Read the benchmark record](${`https://github.com/hassanvfx/mac-ai/blob/main/${lab.benchmark}`})\n- [Read the chapter](/mac-ai/course/${slug})\n\n### Move the lab to your Mac\n\nScan this page’s QR code with your phone, then use Safari Share → AirDrop to send the link to your Mac. Clone the repository once, install the documented \`uv\` group, and run the command above from the repository root.\n`);
}
