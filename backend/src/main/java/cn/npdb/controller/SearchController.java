package cn.npdb.controller;

import cn.npdb.common.ApiResponse;
import cn.npdb.dto.SearchResponse;
import cn.npdb.entity.NaturalProductDetailView;
import cn.npdb.entity.TargetDetailView;
import cn.npdb.mapper.NaturalProductDetailMapper;
import cn.npdb.mapper.TargetDetailMapper;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collections;
import java.util.List;

@RestController
@RequestMapping("/api")
public class SearchController {
    private static final int LIMIT = 20;

    private final NaturalProductDetailMapper naturalProductDetailMapper;
    private final TargetDetailMapper targetDetailMapper;

    public SearchController(NaturalProductDetailMapper naturalProductDetailMapper,
                            TargetDetailMapper targetDetailMapper) {
        this.naturalProductDetailMapper = naturalProductDetailMapper;
        this.targetDetailMapper = targetDetailMapper;
    }

    @GetMapping("/search")
    public ApiResponse<SearchResponse> search(
            @RequestParam("q") String q,
            @RequestParam(value = "type", defaultValue = "all") String type
    ) {
        if (!StringUtils.hasText(q)) {
            return ApiResponse.ok(new SearchResponse(Collections.emptyList(), Collections.emptyList()));
        }
        String keyword = q.trim();
        List<NaturalProductDetailView> nps = Collections.emptyList();
        List<TargetDetailView> targets = Collections.emptyList();

        if ("natural_product".equalsIgnoreCase(type) || "all".equalsIgnoreCase(type)) {
            nps = naturalProductDetailMapper.selectList(
                    new QueryWrapper<NaturalProductDetailView>()
                            .like("pref_name", keyword)
                            .or().like("np_id", keyword)
                            .orderByDesc("id")
                            .last("limit " + LIMIT));
        }
        if ("target".equalsIgnoreCase(type) || "all".equalsIgnoreCase(type)) {
            targets = targetDetailMapper.selectList(
                    new QueryWrapper<TargetDetailView>()
                            .like("target_name", keyword)
                            .or().like("target_id", keyword)
                            .orderByDesc("id")
                            .last("limit " + LIMIT));
        }

        return ApiResponse.ok(new SearchResponse(nps, targets));
    }
}
