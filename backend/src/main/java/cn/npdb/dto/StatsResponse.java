package cn.npdb.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class StatsResponse {
    private long naturalProducts;
    private long targets;
    private long bioactivity;
    private long bioResources;
    private long prescriptions;
    private long diseases;
}
