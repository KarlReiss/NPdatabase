package cn.npdb.dto;

import cn.npdb.entity.NaturalProductDetailView;
import cn.npdb.entity.TargetDetailView;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SearchResponse {
    private List<NaturalProductDetailView> naturalProducts;
    private List<TargetDetailView> targets;
}
