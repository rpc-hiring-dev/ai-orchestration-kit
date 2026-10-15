# Parked tools

Saved for when builds start. Add each one to a project only when that project needs it, because every connector costs tokens in every session.

| Tool | Use it when | How to add |
|---|---|---|
| [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Any project with a UI. It generates a design system from bundled style, palette and font data. | `npx ui-ux-pro-max-cli init --ai claude` in the project |
| [Agent Reach](https://github.com/Panniantong/Agent-Reach) | The researcher needs web search or page reading beyond the built-in tools: Exa search, Jina page reader, YouTube subtitles, RSS. The owner's preferred research tool. | `pip install git+https://github.com/Panniantong/Agent-Reach.git`, then `agent-reach doctor`. Exa search also needs `npx mcporter config add exa https://mcp.exa.ai/mcp`. Cloud environments must allow `mcp.exa.ai` and `r.jina.ai`. |
| [Graphify](https://github.com/Graphify-Labs/graphify) | The codebase is big enough that agents waste time searching | `uv tool install graphifyy`, then `graphify install` |
| [Motion AI Kit](https://motion.dev/docs/ai-kit-install) | The project uses the Motion animation library | `npx motion-ai` |
| [Watermelon UI](https://github.com/WatermelonCorp/watermelon-platform) | A React or shadcn front end that needs ready-made blocks | Hosted connector at `https://mcp.watermelon.sh/mcp` |
| [bklit-ui](https://github.com/bklit/bklit-ui) | Charts, such as a richer dashboard | `npx shadcn@latest add @bklit/line-chart` |
| [Tabler icons](https://github.com/tabler/tabler-icons) | The default icon set | Add it as a project dependency |
| [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) | Only if Graphify isn't enough. Its first run is expensive. | Claude Code plugin |
| [Caveman](https://github.com/JuliusBrussee/caveman) | Probably never. Its terse output and extra rules often cost more than they save. | |
| [unlumen UI](https://ui.unlumen.com/docs) | If you like its look | Copy components from its docs |
| [Swishy](https://www.swishy.ai/) | Animated social or marketing clips | Web app, used by hand |
| [ASCII studio](http://ascii.krackeddevs.com/) | ASCII art from text or photos | Web app, used by hand |
| [FLUID](http://fluid.krackeddevs.com/) | Generative backgrounds and link-preview images | Web app, or its npm embed |
| [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Looking for a skill we don't have yet | Browse, then copy one skill in |
