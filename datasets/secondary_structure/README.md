# RNA 二级结构数据

## 归档范围与下载来源

`data/` 中四个压缩包来自 **MXfold2 作者维护的 v0.1.1 发布页**：

<https://github.com/mxfold/mxfold2/releases/tag/v0.1.1>

MXfold2 的代码与论文提供这些处理后的基准版本。它不是所有结构记录的最初产生者；bpRNA、Rfam、ArchiveII 和 RNAStrAlign 各有上游来源。完整出处见 [source_catalog.csv](source_catalog.csv) 与[文献目录](../../literature/README.md)。

| 压缩包 / 划分 | 包中 BPSEQ 条数 | 通过索引检查 | 长度范围 nt | 用途 |
|---|---:|---:|---:|---|
| bpRNA / TR0 | 10,814 | 10,814 | 33–498 | 训练 |
| bpRNA / VL0 | 1,300 | 1,300 | 33–497 | 验证、选择超参数 |
| bpRNA / TS0 | 1,305 | 1,305 | 22–499 | 保留测试 |
| bpRNA-new | 5,401 | 5,401 | 33–489 | 跨家族补充评估 |
| ArchiveII | 3,966 | 3,966 | 28–1,800 | 清理重叠后的补充评估 |
| RNAStrAlign600-train | 20,923 | 20,856 | 30–600（通过检查的记录） | 可选的训练扩充 |

共 43,709 条源记录，43,642 条通过本次严格索引检查。这里的数量是**记录数，不是跨数据包去重后的独立分子数**。RNAStrAlign 包是长度筛选后的训练子集，不是完整约 37,149 条的母数据集。bpRNA 包也不是完整 102,318 条的 bpRNA-1m。

## 本次检查发现

- bpRNA 的 TR0/VL0/TS0 之间，以及它们与 bpRNA-new 之间，未发现完全相同的标准化序列。
- ArchiveII 与 bpRNA TR0 有 **732 条唯一序列完全相同**，不能直接作为独立测试集。
- RNAStrAlign 与 bpRNA TR0 有 **498 条唯一序列完全相同**。
- ArchiveII 内有 515 条重复序列记录；通过检查的 RNAStrAlign 内有 4,307 条重复序列记录。部分相同序列有不同配对标注，不能未经判断便覆盖。
- RNAStrAlign 有 67 条记录未通过严格 BPSEQ 索引检查：18 条配对索引越界或自配对检查失败，22 条位置索引或单碱基字段检查失败，27 条配对不对称。原始包完整保留，这些记录未输出到 `processed/`，细节见 `dataset_audit.json`。
- bpRNA 三个划分合计 163 条、bpRNA-new 13 条、通过检查的 RNAStrAlign 1,617 条含 A/C/G/U 以外字符。它们已标记并保留，正式训练前需确定处理规则。

**完全一致检查不能替代同源性、家族泄漏或 EVA 预训练重叠检查。** 不应将这里的测试集自动称为“EVA 从未见过”。

## 结构标签的含义

这些是来源混合的参考结构，涉及比较序列分析、家族共识与实验结构等，不能统称为全部直接实验测得的 circRNA 配对真值。

本次 bpRNA 和 bpRNA-new 使用 MXfold2 发布的 canonicalized 版本；检查未发现交叉配对或非 AU/CG/GU 配对。ArchiveII 和 RNAStrAlign 中仍有交叉配对，后者还包含非规范或涉及模糊字符的配对。不同版本不能不加说明地混合比较。

SHAPE-MaP 测得的是每个位点的化学反应性。它可约束结构推断，但不是直接给出完整的碱基配对矩阵。circAtlas 3.0 的二级结构说明使用 RNAfold 预测，这类标签也不能作为独立实验真值。

## 统一格式

`processed/*.jsonl.gz` 每行是一条 JSON，保留：

- `id`、`split`、`source_archive`、`source_member`：来源与原始划分。
- `sequence_original`：原序列；`sequence`：转大写并将 T 转 U 的序列。
- `partner_index_1based`：每个位点的配对位置，**从 1 开始；0 表示未配对**。
- `length`、`base_pair_count`、`ambiguous_symbols`、`crossing_pairs_present`、`noncanonical_pair_count`：检查信息。
- `sequence_sha256`：标准化序列的哈希。
- `topology`：`not_verified_as_circular`，避免把通用 RNA 数据误标为 circRNA。

没有修改、对称化或补全原始配对标签，也没有重新随机划分数据。索引检查失败的记录保留在原始压缩包并记入错误清单。

## 复现

只需 Python 标准库。在仓库根目录：

```bash
# 检查原始包；如果缺失，则按已记录的版本、URL、SHA-256 下载。
python datasets/secondary_structure/tools/download_sources.py

# 只核验本地包，不联网。
python datasets/secondary_structure/tools/download_sources.py --verify-only

# 保留源包，重建统一格式和质量检查报告。
python datasets/secondary_structure/tools/audit_datasets.py
```

所有下载与归档状态以具体文件和清单为准。尚未取得的补充来源会在对应清单中标记，不计入上表。
