"""Internal Research fixture for the first local persistence proof."""

INTERNAL_RESEARCH_WORKSPACE_ID = "ws_internal_research_001"

INTERNAL_RESEARCH_WORKSPACE_CONFIG = {
    "workspace_name": "Neon Ronin Internal Research",
    "workspace_type": "internal_research",
    "status": "manual_test",
    "purpose": "Research and evaluate business ideas, platform decisions, and opportunity signals before onboarding real business workspaces.",
    "channels": ["internal_research"],
    "adapter": "internal-research-workspace",
    "allowed_agents": [],
    "review_gates": [
        "quality_gate",
        "strategy_review_gate",
        "data_boundary_gate",
        "promotion_readiness_gate",
    ],
    "observatory": {
        "query_allowed": False,
        "submit_allowed": False,
        "live_ingestion_allowed": False,
    },
    "storage_rules": {
        "local_only": True,
        "customer_data_allowed": False,
        "provider_payloads_allowed": False,
    },
    "runtime": {
        "default_mode": "off",
        "allowed_modes": ["off"],
        "scheduled_allowed": False,
        "watch_mode_allowed": False,
    },
    "hard_no_rules": [
        "no_external_writes",
        "no_agents",
        "no_scheduled_jobs",
        "no_watch_mode",
        "no_live_observatory_ingestion",
    ],
    "audit_requirements": [
        "workspace_config_created",
        "audit_first_write_required",
    ],
    "external_references": [],
}