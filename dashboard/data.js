window.SKILL_DASHBOARD_DATA = {
  "generatedAt": "2026-06-09T03:57:06.034960+00:00",
  "skill": "ai-video-creator-style",
  "iteration": "iteration-001",
  "cases": 12,
  "metrics": [
    {
      "config": "without_skill",
      "label": "无 Skill",
      "passRate": 16.7,
      "triggerRecall": null,
      "overTriggerRate": null,
      "avgTokens": 720,
      "avgDurationMs": 480
    },
    {
      "config": "with_skill_v1",
      "label": "Skill v1",
      "passRate": 75.0,
      "triggerRecall": 80.0,
      "overTriggerRate": 50.0,
      "avgTokens": 1142.5,
      "avgDurationMs": 827.5
    },
    {
      "config": "with_skill_v2",
      "label": "Skill v2",
      "passRate": 100.0,
      "triggerRecall": 100.0,
      "overTriggerRate": 0,
      "avgTokens": 935,
      "avgDurationMs": 625
    }
  ],
  "headline": {
    "passLiftV2VsBase": 83.3,
    "passLiftV2VsV1": 25.0,
    "overTriggerDrop": 50.0,
    "tokenDeltaV2VsV1": -18.2
  },
  "failurePatterns": [
    {
      "pattern": "产出不完整",
      "withoutSkill": 10,
      "skillV1": 3,
      "skillV2": 0
    },
    {
      "pattern": "效率成本偏高",
      "withoutSkill": 0,
      "skillV1": 9,
      "skillV2": 0
    },
    {
      "pattern": "泛化风险",
      "withoutSkill": 4,
      "skillV1": 2,
      "skillV2": 0
    },
    {
      "pattern": "触发不匹配",
      "withoutSkill": 0,
      "skillV1": 3,
      "skillV2": 0
    },
    {
      "pattern": "风格较弱",
      "withoutSkill": 10,
      "skillV1": 10,
      "skillV2": 0
    }
  ],
  "caseTypes": [
    {
      "type": "boundary",
      "label": "边界",
      "count": 2
    },
    {
      "type": "core",
      "label": "核心",
      "count": 6
    },
    {
      "type": "extension",
      "label": "扩展",
      "count": 2
    },
    {
      "type": "negative",
      "label": "负向",
      "count": 2
    }
  ],
  "topBadcasesV1": [
    {
      "caseId": "boundary-sparse-brief",
      "caseType": "boundary",
      "score": 20.0,
      "failurePatterns": [
        "触发不匹配",
        "产出不完整",
        "风格较弱",
        "泛化风险"
      ]
    },
    {
      "caseId": "extension-cover-only",
      "caseType": "extension",
      "score": 20.0,
      "failurePatterns": [
        "触发不匹配",
        "产出不完整",
        "风格较弱",
        "泛化风险"
      ]
    },
    {
      "caseId": "negative-press-release",
      "caseType": "negative",
      "score": 50.0,
      "failurePatterns": [
        "触发不匹配",
        "产出不完整",
        "效率成本偏高"
      ]
    }
  ],
  "topBadcasesV2": [],
  "caseMatrix": [
    {
      "caseId": "core-skill-eval-lab",
      "caseType": "core",
      "shouldTrigger": true,
      "configs": {
        "without_skill": {
          "pass": false,
          "score": 50.0,
          "triggered": false,
          "tokens": 760,
          "durationMs": 480,
          "failurePatterns": [
            "产出不完整",
            "风格较弱"
          ]
        },
        "with_skill_v1": {
          "pass": true,
          "score": 70.0,
          "triggered": true,
          "tokens": 1250,
          "durationMs": 930,
          "failurePatterns": [
            "风格较弱",
            "效率成本偏高"
          ]
        },
        "with_skill_v2": {
          "pass": true,
          "score": 100.0,
          "triggered": true,
          "tokens": 1010,
          "durationMs": 650,
          "failurePatterns": []
        }
      }
    },
    {
      "caseId": "core-agent-coding",
      "caseType": "core",
      "shouldTrigger": true,
      "configs": {
        "without_skill": {
          "pass": false,
          "score": 50.0,
          "triggered": false,
          "tokens": 760,
          "durationMs": 480,
          "failurePatterns": [
            "产出不完整",
            "风格较弱"
          ]
        },
        "with_skill_v1": {
          "pass": true,
          "score": 70.0,
          "triggered": true,
          "tokens": 1250,
          "durationMs": 930,
          "failurePatterns": [
            "风格较弱",
            "效率成本偏高"
          ]
        },
        "with_skill_v2": {
          "pass": true,
          "score": 100.0,
          "triggered": true,
          "tokens": 1010,
          "durationMs": 650,
          "failurePatterns": []
        }
      }
    },
    {
      "caseId": "core-mcp-db",
      "caseType": "core",
      "shouldTrigger": true,
      "configs": {
        "without_skill": {
          "pass": false,
          "score": 50.0,
          "triggered": false,
          "tokens": 760,
          "durationMs": 480,
          "failurePatterns": [
            "产出不完整",
            "风格较弱"
          ]
        },
        "with_skill_v1": {
          "pass": true,
          "score": 70.0,
          "triggered": true,
          "tokens": 1250,
          "durationMs": 930,
          "failurePatterns": [
            "风格较弱",
            "效率成本偏高"
          ]
        },
        "with_skill_v2": {
          "pass": true,
          "score": 100.0,
          "triggered": true,
          "tokens": 1010,
          "durationMs": 650,
          "failurePatterns": []
        }
      }
    },
    {
      "caseId": "core-ai-image",
      "caseType": "core",
      "shouldTrigger": true,
      "configs": {
        "without_skill": {
          "pass": false,
          "score": 50.0,
          "triggered": false,
          "tokens": 760,
          "durationMs": 480,
          "failurePatterns": [
            "产出不完整",
            "风格较弱"
          ]
        },
        "with_skill_v1": {
          "pass": true,
          "score": 70.0,
          "triggered": true,
          "tokens": 1250,
          "durationMs": 930,
          "failurePatterns": [
            "风格较弱",
            "效率成本偏高"
          ]
        },
        "with_skill_v2": {
          "pass": true,
          "score": 100.0,
          "triggered": true,
          "tokens": 1010,
          "durationMs": 650,
          "failurePatterns": []
        }
      }
    },
    {
      "caseId": "core-cloud-inference",
      "caseType": "core",
      "shouldTrigger": true,
      "configs": {
        "without_skill": {
          "pass": false,
          "score": 50.0,
          "triggered": false,
          "tokens": 760,
          "durationMs": 480,
          "failurePatterns": [
            "产出不完整",
            "风格较弱"
          ]
        },
        "with_skill_v1": {
          "pass": true,
          "score": 70.0,
          "triggered": true,
          "tokens": 1250,
          "durationMs": 930,
          "failurePatterns": [
            "风格较弱",
            "效率成本偏高"
          ]
        },
        "with_skill_v2": {
          "pass": true,
          "score": 100.0,
          "triggered": true,
          "tokens": 1010,
          "durationMs": 650,
          "failurePatterns": []
        }
      }
    },
    {
      "caseId": "core-meeting-agent",
      "caseType": "core",
      "shouldTrigger": true,
      "configs": {
        "without_skill": {
          "pass": false,
          "score": 50.0,
          "triggered": false,
          "tokens": 760,
          "durationMs": 480,
          "failurePatterns": [
            "产出不完整",
            "风格较弱"
          ]
        },
        "with_skill_v1": {
          "pass": true,
          "score": 70.0,
          "triggered": true,
          "tokens": 1250,
          "durationMs": 930,
          "failurePatterns": [
            "风格较弱",
            "效率成本偏高"
          ]
        },
        "with_skill_v2": {
          "pass": true,
          "score": 100.0,
          "triggered": true,
          "tokens": 1010,
          "durationMs": 650,
          "failurePatterns": []
        }
      }
    },
    {
      "caseId": "boundary-sparse-brief",
      "caseType": "boundary",
      "shouldTrigger": true,
      "configs": {
        "without_skill": {
          "pass": false,
          "score": 25.0,
          "triggered": false,
          "tokens": 760,
          "durationMs": 480,
          "failurePatterns": [
            "产出不完整",
            "风格较弱",
            "泛化风险"
          ]
        },
        "with_skill_v1": {
          "pass": false,
          "score": 20.0,
          "triggered": false,
          "tokens": 820,
          "durationMs": 520,
          "failurePatterns": [
            "触发不匹配",
            "产出不完整",
            "风格较弱",
            "泛化风险"
          ]
        },
        "with_skill_v2": {
          "pass": true,
          "score": 100.0,
          "triggered": true,
          "tokens": 1010,
          "durationMs": 650,
          "failurePatterns": []
        }
      }
    },
    {
      "caseId": "boundary-complex-brief",
      "caseType": "boundary",
      "shouldTrigger": true,
      "configs": {
        "without_skill": {
          "pass": false,
          "score": 25.0,
          "triggered": false,
          "tokens": 760,
          "durationMs": 480,
          "failurePatterns": [
            "产出不完整",
            "风格较弱",
            "泛化风险"
          ]
        },
        "with_skill_v1": {
          "pass": true,
          "score": 70.0,
          "triggered": true,
          "tokens": 1250,
          "durationMs": 930,
          "failurePatterns": [
            "风格较弱",
            "效率成本偏高"
          ]
        },
        "with_skill_v2": {
          "pass": true,
          "score": 100.0,
          "triggered": true,
          "tokens": 1010,
          "durationMs": 650,
          "failurePatterns": []
        }
      }
    },
    {
      "caseId": "extension-title-pool",
      "caseType": "extension",
      "shouldTrigger": true,
      "configs": {
        "without_skill": {
          "pass": false,
          "score": 25.0,
          "triggered": false,
          "tokens": 760,
          "durationMs": 480,
          "failurePatterns": [
            "产出不完整",
            "风格较弱",
            "泛化风险"
          ]
        },
        "with_skill_v1": {
          "pass": true,
          "score": 70.0,
          "triggered": true,
          "tokens": 1250,
          "durationMs": 930,
          "failurePatterns": [
            "风格较弱",
            "效率成本偏高"
          ]
        },
        "with_skill_v2": {
          "pass": true,
          "score": 100.0,
          "triggered": true,
          "tokens": 1010,
          "durationMs": 650,
          "failurePatterns": []
        }
      }
    },
    {
      "caseId": "extension-cover-only",
      "caseType": "extension",
      "shouldTrigger": true,
      "configs": {
        "without_skill": {
          "pass": false,
          "score": 25.0,
          "triggered": false,
          "tokens": 760,
          "durationMs": 480,
          "failurePatterns": [
            "产出不完整",
            "风格较弱",
            "泛化风险"
          ]
        },
        "with_skill_v1": {
          "pass": false,
          "score": 20.0,
          "triggered": false,
          "tokens": 820,
          "durationMs": 520,
          "failurePatterns": [
            "触发不匹配",
            "产出不完整",
            "风格较弱",
            "泛化风险"
          ]
        },
        "with_skill_v2": {
          "pass": true,
          "score": 100.0,
          "triggered": true,
          "tokens": 1010,
          "durationMs": 650,
          "failurePatterns": []
        }
      }
    },
    {
      "caseId": "negative-press-release",
      "caseType": "negative",
      "shouldTrigger": false,
      "configs": {
        "without_skill": {
          "pass": true,
          "score": 100.0,
          "triggered": false,
          "tokens": 520,
          "durationMs": 480,
          "failurePatterns": []
        },
        "with_skill_v1": {
          "pass": false,
          "score": 50.0,
          "triggered": true,
          "tokens": 1250,
          "durationMs": 930,
          "failurePatterns": [
            "触发不匹配",
            "产出不完整",
            "效率成本偏高"
          ]
        },
        "with_skill_v2": {
          "pass": true,
          "score": 100.0,
          "triggered": false,
          "tokens": 560,
          "durationMs": 500,
          "failurePatterns": []
        }
      }
    },
    {
      "caseId": "negative-project-plan",
      "caseType": "negative",
      "shouldTrigger": false,
      "configs": {
        "without_skill": {
          "pass": true,
          "score": 100.0,
          "triggered": false,
          "tokens": 520,
          "durationMs": 480,
          "failurePatterns": []
        },
        "with_skill_v1": {
          "pass": true,
          "score": 100.0,
          "triggered": false,
          "tokens": 820,
          "durationMs": 520,
          "failurePatterns": []
        },
        "with_skill_v2": {
          "pass": true,
          "score": 100.0,
          "triggered": false,
          "tokens": 560,
          "durationMs": 500,
          "failurePatterns": []
        }
      }
    }
  ],
  "versions": [
    {
      "version": "v1",
      "changed_parts": [
        "初版 SKILL.md"
      ],
      "main_hypothesis": "宽泛的 AI 产品视频 Skill 可以相对无 Skill 基线提升完整创意包生成质量。",
      "known_risks": [
        "description 过宽",
        "负向边界较弱",
        "没有确定性输出校验器",
        "风格规则没有硬化"
      ],
      "iteration": "iteration-001",
      "observed_metrics": {
        "pass_rate": 0.75,
        "trigger_recall": 0.8,
        "over_trigger_rate": 0.5,
        "avg_tokens": 1142
      },
      "decision": "继续迭代"
    },
    {
      "version": "v2",
      "changed_parts": [
        "description",
        "SKILL.md 检查清单",
        "scripts/validate_package.py"
      ],
      "main_hypothesis": "增加触发边界、显式产出契约和确定性检查，可以在提升质量的同时减少无效上下文消耗。",
      "known_risks": [
        "上线前需要把模拟评测替换成真实大模型调用",
        "样例集还需要补充更多历史真实产品信息"
      ],
      "iteration": "iteration-001",
      "observed_metrics": {
        "pass_rate": 1.0,
        "trigger_recall": 1.0,
        "over_trigger_rate": 0.0,
        "avg_tokens": 935
      },
      "decision": "发布 MVP"
    }
  ],
  "reasonArchive": [
    {
      "case_id": "boundary-sparse-brief",
      "run_config": "with_skill_v1",
      "human_expected": "信息很少时也应该触发视频创作 Skill，并只在内部补齐必要澄清。",
      "observed_behavior": "v1 没有触发，退回到了通用产品内容方案。",
      "failure_pattern": "触发不匹配",
      "root_cause": "description 依赖显式的视频或产品措辞，没有覆盖稀疏的创作者风格请求。",
      "suggested_action": "扩展 description，覆盖创作者产品信息、B 站视频标题、封面、Demo、大纲或口播稿请求。",
      "should_regress": true
    },
    {
      "case_id": "extension-cover-only",
      "run_config": "with_skill_v1",
      "human_expected": "只要封面文案的请求也应该触发 Skill，并加载封面专项规则。",
      "observed_behavior": "v1 因为请求没有被表述成完整视频创意包而漏触发。",
      "failure_pattern": "触发不匹配",
      "root_cause": "description 没有把封面文案明确列为直接触发条件。",
      "suggested_action": "把封面文案、缩略图文案、标题封面搭配加入触发条件。",
      "should_regress": true
    },
    {
      "case_id": "negative-press-release",
      "run_config": "with_skill_v1",
      "human_expected": "正式新闻稿写作不应该触发 B 站视频创作 Skill。",
      "observed_behavior": "v1 因为 description 写了 AI 产品宣传内容而误触发。",
      "failure_pattern": "过度触发",
      "root_cause": "description 缺少新闻稿和通用非视频营销文案的负向边界。",
      "suggested_action": "为新闻稿、官方文章、项目计划和非视频内容增加明确的禁用边界。",
      "should_regress": true
    }
  ],
  "regressionSet": {
    "skill": "ai-video-creator-style",
    "iteration": "iteration-001",
    "must_keep_cases": [
      "boundary-sparse-brief",
      "extension-cover-only",
      "negative-press-release",
      "negative-project-plan"
    ],
    "reason": "这些样例用于保护触发召回、只要封面文案的扩展能力，以及防止过度触发。"
  }
};
