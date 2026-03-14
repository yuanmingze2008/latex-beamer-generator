# latex-beamer-generator

`latex-beamer-generator` 是一个面向 agent 的开源 skill 项目，用于生成学术风格的 LaTeX Beamer 演示文稿。

这个仓库的设计目标不是做一个面向终端用户的独立桌面工具，而是提供一套可复用的 skill 规范、参考资料、模板资源和辅助脚本，使支持 skill 的 agent 能稳定完成学术 slides 生成任务。

主要规范见 [`SKILL.md`](SKILL.md)。`agents/openai.yaml` 仅作为特定生态中的兼容元数据，不是主规范。

## 这个 Skill 能做什么

这个 skill 适合以下场景：

- 用户需要学术汇报、课程报告、组会、答辩、seminar、research talk 等 slides
- 用户想把学术 PPT 或 PDF 需求转成 Beamer 工作流
- 用户只有主题，希望 agent 帮忙规划并生成整套 slides 内容
- 用户已经有论文摘要、笔记、文档等材料，希望 agent 压缩整理成 slides
- 用户提供了截图、PNG、PDF 页面图等非文本材料，并由 agent 先做理解后再进入生成流程

当前版本支持：

- 根据主题生成 slide 内容
- 根据已有材料生成 slide 内容
- 多种常见 Beamer 主题
- 根据页数与复杂度在单文件和多文件输出之间切换
- 生成可编辑的 Beamer 项目，而不是一次性不可维护的产物

## 仓库结构

```text
latex-beamer-generator/
  SKILL.md
  README.md
  README.zh-CN.md
  agents/
    openai.yaml
  references/
    workflow.md
    content-generation.md
    beamer-themes.md
  assets/
    templates/
    theme-presets/
  scripts/
    normalize_source_input.py
    generate_beamer_project.py
    compile_beamer_project.py
  examples/
    sample_requests.md
    sample_outputs.md
```

## 核心文件说明

- [`SKILL.md`](SKILL.md)：主行为规范，定义 skill 的触发条件、追问顺序、输入模式、输出策略
- [`agents/openai.yaml`](agents/openai.yaml)：可选兼容元数据，用于支持 skill 展示的生态
- [`references/workflow.md`](references/workflow.md)：从用户请求到内部 spec 再到 Beamer 输出的流程说明
- [`references/content-generation.md`](references/content-generation.md)：正文生成的两条主路径与非文本源处理约定
- [`references/beamer-themes.md`](references/beamer-themes.md)：支持的主题及默认选择策略
- [`scripts/normalize_source_input.py`](scripts/normalize_source_input.py)：将松散输入整理成更稳定的生成 spec
- [`scripts/generate_beamer_project.py`](scripts/generate_beamer_project.py)：根据 spec 生成 Beamer 项目
- [`scripts/compile_beamer_project.py`](scripts/compile_beamer_project.py)：使用 `latexmk` 编译生成的项目

## 运行环境

如果你想在本地直接运行辅助脚本，需要准备：

- Python 3.10 或更高版本
- LaTeX 工具链，以及可用的 `latexmk`

可选检查命令：

```powershell
python --version
latexmk -v
```

## 本地最小使用流程

如果你希望不依赖外部 agent，直接在本地验证脚本链路，可以使用下面的最小流程：

```powershell
python scripts\normalize_source_input.py --spec path\to\spec.json --output generated\normalized.json
python scripts\generate_beamer_project.py --spec generated\normalized.json --output-dir generated\deck
python scripts\compile_beamer_project.py --project-dir generated\deck
```

如果你只想拿到 `.tex` 文件而不编译 PDF，可以跳过最后一步。

## 设计原则

这个仓库遵循以下原则：

- `SKILL.md` 是主规范
- `agents/openai.yaml` 只是兼容层，不负责定义核心行为
- `scripts/` 是辅助执行层，不替代 agent 的产品决策
- 非文本材料的视觉理解由 agent 或模型先完成，再转成结构化描述交给 skill 使用
- 小中型 deck 默认优先单文件，大型或复杂 deck 才拆为多文件

## 开源定位

这个项目应当作为“通用 agent skill”被理解，而不是某个单一平台的私有工具：

- 即使某个 agent 不认识 `agents/openai.yaml`
- 只要它能读取 `SKILL.md` 并使用仓库中的参考资料、模板和脚本
- 它仍然可以利用这个 skill 完成学术 Beamer 生成任务

## 当前版本重点

当前版本主要聚焦于：

- 学术 slides 请求的触发与追问
- 两种正文生成模式
- 多主题支持
- 单文件与多文件输出策略
- 可在本地直接验证的最小脚本流程

后续可以继续增强：

- 更强的 slide 结构规划
- bibliography / figure / table 的更完整组织能力
- 更丰富的主题 preset
- 更细粒度的长文档内容压缩与抽取
