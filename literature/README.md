# 论文与引用

本目录整理了五篇与归档数据直接相关的论文。**目前保存的是引用、DOI、公开全文链接与获取状态，PDF 文件数量为 0。** 云环境的网络白名单拦截了学术站点下载；按研究者要求，先归档原文链接。

| 论文 | 与本项目的关系 | 原文入口 |
|---|---|---|
| **Sato, Akiyama & Sakakibara (2021)**. RNA secondary structure prediction using deep learning with thermodynamic integration. *Nature Communications* 12, 941. | MXfold2 方法；本次四个数据包的发布来源；bpRNA-new 的相关研究 | [DOI](https://doi.org/10.1038/s41467-021-21194-4) · [PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC7878809/) · [PDF](https://www.nature.com/articles/s41467-021-21194-4.pdf) |
| **Danaee et al. (2018)**. bpRNA: large-scale automated annotation and analysis of RNA secondary structure. *Nucleic Acids Research* 46(11), 5381–5394. | bpRNA 注释工具与 bpRNA-1m 母数据库 | [DOI](https://doi.org/10.1093/nar/gky285) · [PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC6009582/) · [PDF](https://academic.oup.com/nar/article-pdf/46/11/5381/27982344/gky285.pdf) |
| **Tan et al. (2017)**. TurboFold II: RNA structural alignment and secondary structure prediction informed by multiple homologs. *Nucleic Acids Research* 45(20), 11570–11581. | RNAStrAlign 上游研究；本仓库保存的是 MXfold2 的长度筛选训练子集 | [DOI](https://doi.org/10.1093/nar/gkx815) · [PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC5714223/) · [PDF](https://academic.oup.com/nar/article-pdf/45/20/11570/21743179/gkx815.pdf) |
| **Sloma & Mathews (2016)**. Exact calculation of loop formation probability identifies folding motifs in RNA secondary structures. *RNA* 22(12), 1808–1818. | ArchiveII 常用原始引用 | [DOI](https://doi.org/10.1261/rna.053694.115) · [PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC5113201/) · [PDF](https://rnajournal.cshlp.org/content/22/12/1808.full.pdf) |
| **Liu et al. (2019)**. Structure and Degradation of Circular RNAs Regulate PKR Activation in Innate Immunity. *Cell* 177(4), 865–880.e21. | circRNA 实验结构研究；GSE126195 / PRJNA521266 的关联论文 | [DOI](https://doi.org/10.1016/j.cell.2019.03.046) · [作者提供的全文](https://yanglab.github.io/static/publication_pdf/2019_Cell-circRNAs_PKR.pdf) · [NCBI 数据记录](https://www.ncbi.nlm.nih.gov/bioproject/521266) |

完整作者、刊期、页码、许可证据和文件获取状态见 [papers.json](papers.json)。可直接导入文献管理工具的引用见 [references.bib](references.bib)。

## 怎样使用这些文献

1. 用 MXfold2 论文和作者发布页确认具体基准版本、数据划分和处理方式。
2. 用 bpRNA、TurboFold II、Sloma & Mathews 三篇追溯对应数据的来源和结构标注方法。
3. 用 Cell 论文了解 circRNA 的实验依据。SHAPE 反应性与实验约束下推断的结构需要分别报告。

数据下载出处不等于数据原始出处；正式报告应同时引用使用的基准处理版本和相关上游文献。

## 许可与 PDF 获取

已核实原文许可：MXfold2、TurboFold II 为 CC BY 4.0；bpRNA、Sloma & Mathews 为 CC BY-NC 4.0，后者首年限制期已过。第三方插图等可能另有条款，具体证据见 `papers.json`。

Cell 作者公开了全文链接，但未确认可公开再分发的许可，因此本仓库仅保存原文链接和引用。

以后在允许访问来源站点的网络中，可对四篇开放许可论文运行：

```bash
python literature/download_papers.py
```

脚本使用正常代理和 TLS 校验，验证 PDF 文件头、结束标记并记录 SHA-256；不会下载标记为 `link_only` 的条目。该检查只能排除明显的 HTML 错误页或不完整文件，不替代人工核对论文内容。下载后需重新更新仓库完整性清单，再提交新增文件。

**链接已收录不代表 PDF 已下载，也不保证出版社 URL 永久不变；DOI 是优先的稳定入口。**
