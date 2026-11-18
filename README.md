# LLM-for-circRNA

circRNA 表示学习与 RNA 二级结构评估的研究资料仓库。

## 从这里开始

| 内容 | 入口 |
|---|---|
| 数据来源、版本和使用边界 | [二级结构数据说明](datasets/secondary_structure/README.md) |
| 四个原始压缩包 | [data/](datasets/secondary_structure/data/) |
| 母库部分备份、补充数据入口 | [supplementary/](datasets/secondary_structure/supplementary/) |
| 六份统一格式的数据 | [processed/](datasets/secondary_structure/processed/) |
| 文件数量、长度与重复检查 | [汇总 CSV](datasets/secondary_structure/dataset_summary.csv)、[完整检查 JSON](datasets/secondary_structure/dataset_audit.json) |
| 论文原文、引文与获取状态 | [文献目录](literature/README.md) |
| 检查及重新下载脚本 | [数据工具](datasets/secondary_structure/tools/) |

数据保留原始文件与固定的发布版本。`processed/` 仅统一存储格式并检查配对索引，不代表已完成同源性去重、预训练污染排查或生物学真值验证。

## 研究用途

这些序列—结构数据用于评估 RNA 表示是否包含碱基配对信息。建议首先使用 bpRNA 原有的 TR0 / VL0 / TS0 划分，再用 bpRNA-new 补充跨家族评估。真正 circRNA 的循环移位等变性需要单独验证，不能直接把线性 RNA 首尾相接并视为同一个分子。

本仓库当前归档的是数据与文献材料；当前服务器上的训练状态需实时查询，不由这份资料归档推断。

## 文件与来源核验

在仓库根目录运行：

```bash
python tools/verify_archive.py
python datasets/secondary_structure/tools/download_sources.py --verify-only
```

重新生成统一格式与检查报告：

```bash
python datasets/secondary_structure/tools/audit_datasets.py
```

来源网址和原始包 SHA-256 保存在数据检查报告中，仓库文件的完整性记录见 [FILE_MANIFEST.json](FILE_MANIFEST.json)。重新生成文件后，内容或压缩文件时间戳可能改变；应重新核验并更新清单。

## 使用与引用

引用实际使用的上游数据库与对应处理版本。第三方数据及论文保留各自版权和许可；作者代码仓库的许可证不能自动替代其中所有数据或论文的许可。具体出处与已核实的许可见数据说明和文献目录。
