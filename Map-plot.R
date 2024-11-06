# 设置工作目录
setwd("/Users/luxiaoxiaobang/Downloads/Beifen/工作/胃滞留药物递送机器人/数学模型-模拟预测影响/预测结果")

# 加载包
library(ggplot2)
library(dplyr)
library(sf)
library(rnaturalearth)
library(rnaturalearthdata)
library(readxl)

# 读取数据
data <- read_excel("2040年应用SGSD后减少的GWP.xlsx")

# 确保 'GWP_reduction' 列是数值类型
data$GWP_reduction <- as.numeric(data$GWP_reduction)

# 查看数据分布的统计摘要
summary(data$GWP_reduction)

# 获取世界地图数据
world <- ne_countries(scale = "medium", returnclass = "sf")

# 使用 code 列合并数据
world_data <- merge(world, data, by.x = "iso_a3", by.y = "Code", all.x = TRUE)

# 根据数据分布重新设定区间，增加红色区间的数量
breaks <- c(0, 500000, 1500000, 5000000, 20000000, 50000000, 200000000, 400000000, Inf)
labels <- c("0-500K", "500K-1.5M", "1.5M-5M", "5M-20M", "20M-50M", "50M-200M", "200M-400M", ">400M")

# 创建区间
world_data$change_category <- cut(world_data$GWP_reduction,
                                  breaks = breaks,
                                  labels = labels,
                                  include.lowest = TRUE)

colors <- c("#61baeb", "#6ac4f0", "#74cff5", "#a7e1f9", "#dff4fd", "#f4b7b9", "#f28d8c", "#f57589")

# 绘制地图
ggplot(data = world_data) +
  geom_sf(aes(fill = change_category), color = "#ede2ec", size = 1) +
  scale_fill_manual(values = colors,
                    na.value = "grey",
                    drop = FALSE) +
  theme_minimal() +
  labs(title = "Global Map Showing GWP Reduction by Country",
       fill = "GWP Reduction") +
  theme(
    axis.title.x = element_text(size = 12),
    axis.title.y = element_text(size = 12),
    axis.text.x = element_text(size = 10),
    axis.text.y = element_text(size = 10),
    panel.grid.major = element_blank(), # 去除大网格线
    panel.grid.minor = element_blank(), # 去除小网格线
    axis.line = element_line(color = "black") # 保留坐标轴的线
  ) +
  coord_sf(xlim = c(-180, 180), ylim = c(-60, 90), expand = FALSE) +
  xlab("Longitude") +
  ylab("Latitude")
