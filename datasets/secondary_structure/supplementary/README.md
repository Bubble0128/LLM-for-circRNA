# 补充来源

## 已归档：bpRNA 作者发布的 SQL Part 1

`Load_bpRNA_1m_Mysql_Part1.zip` 来自 [hendrixlab/bpRNA 官方作者仓库](https://github.com/hendrixlab/bpRNA/tree/master/bpRNA_1m)，大小 39,672,063 bytes，校验值见 [manifest.json](manifest.json)。

它包含重建 bpRNA-1m 数据库所用的 SQL 文件，包括序列、来源及部分结构统计。**这是两部分中的 Part 1，不能单独恢复完整母数据库，也不是即用的完整 BPSEQ / dot-bracket 配对文件。** SQL 未执行。可用于追溯数据来源，但不计入主目录四个基准包的训练记录数。

Part 2 的来源链接和大小（68,625,251 bytes）已记录在清单，未下载。第三方内容保留原权利声明，未为原始数据库核实单独的数据许可。

## 已收录链接，尚未下载

| 来源 | 入口 | 状态及用途 |
|---|---|---|
| bpRNA-1m 完整结构、90% 去冗余子集 | [官方网站](https://bprna.cgrb.oregonstate.edu/download.php) | 官网受当前云网络策略限制；清单中的直接 ZIP 地址仅为公开源码引用的候选，当前下载可用性未验证 |
| GSE126195 / PRJNA521266 | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE126195) · [BioProject](https://www.ncbi.nlm.nih.gov/bioproject/521266) | 处理后补充数据尚未下载；官方报告约 2 MB、46 个实验，实验数不等于独立 circRNA 结构数 |

GSE126195 的 `Norm_profile` 是每个核苷酸的 SHAPE 反应性，不能直接称为碱基配对真值。已核实的样本附件名、官方样本链接和格式说明见 `manifest.json`。没有下载原始测序 reads。
