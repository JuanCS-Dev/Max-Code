# MAXIMUS - Testing Guide

**Gerado:** 2025-11-07 20:47:00

---

## Test Structure Overview

### core

**Test Files:** 798

**Structure:**
```
  - archived_broken/archived_v4_tests/test_arousal_integration_v4.py
  - archived_broken/archived_v4_tests/test_base_v4.py
  - archived_broken/archived_v4_tests/test_contradiction_detector_v4.py
  - archived_broken/archived_v4_tests/test_controller_old_v4.py
  - archived_broken/archived_v4_tests/test_controller_v4.py
  - archived_broken/archived_v4_tests/test_coordinator_old_v4.py
  - archived_broken/archived_v4_tests/test_coordinator_v4.py
  - archived_broken/archived_v4_tests/test_esgt_components.py
  - archived_broken/archived_v4_tests/test_euler_vs_rk4_comparison.py
  - archived_broken/archived_v4_tests/test_fabric_old_v4.py
  - archived_broken/archived_v4_tests/test_fabric_v4.py
  - archived_broken/archived_v4_tests/test_goals_v4.py
  - archived_broken/archived_v4_tests/test_immune_e2e_statistics.py
  - archived_broken/archived_v4_tests/test_introspection_engine_v4.py
  - archived_broken/archived_v4_tests/test_kuramoto_v4.py
  - archived_broken/archived_v4_tests/test_meta_monitor_v4.py
  - archived_broken/archived_v4_tests/test_metrics_monitor_v4.py
  - archived_broken/archived_v4_tests/test_monitor_old_v4.py
  - archived_broken/archived_v4_tests/test_monitor_v4.py
  - archived_broken/archived_v4_tests/test_monte_carlo_statistics.py
  - archived_broken/archived_v4_tests/test_recursive_reasoner_v4.py
  - archived_broken/archived_v4_tests/test_robustness_parameter_sweep.py
  - archived_broken/archived_v4_tests/test_run_controller_coverage_v4.py
  - archived_broken/archived_v4_tests/test_salience_detector_v4.py
  - archived_broken/archived_v4_tests/test_simple_v4.py
  - archived_broken/archived_v4_tests/test_stress_v4.py
  - archived_broken/archived_v4_tests/test_sync_v4.py
  - archived_broken/test_acetylcholine_hardened_v3.py
  - archived_broken/test_acetylcholine_system_v3.py
  - archived_broken/test_action_plan_v3.py
  - archived_broken/test_advanced_tools_v3.py
  - archived_broken/test_adw_router_v3.py
  - archived_broken/test_agent_templates_v3.py
  - archived_broken/test_aggregation_v3.py
  - archived_broken/test_ai_analyzer_v3.py
  - archived_broken/test_all_services_tools_v3.py
  - archived_broken/test_alternatives_v3.py
  - archived_broken/test_api_routes_v3.py
  - archived_broken/test_api_v3.py
  - archived_broken/test_api_websocket_sse.py
  - archived_broken/test_arousal_integration_v3.py
  - archived_broken/test_article_ii_guardian_v3.py
  - archived_broken/test_article_iii_guardian_v3.py
  - archived_broken/test_article_iv_guardian_v3.py
  - archived_broken/test_article_v_guardian_v3.py
  - archived_broken/test_attack_surface_adw_v3.py
  - archived_broken/test_attention_core_v3.py
  - archived_broken/test_attention_schema_v3.py
  - archived_broken/test_audit_infrastructure_v3.py
  - archived_broken/test_audit_trail_v3.py
  - archived_broken/test_audit_v3.py
  - archived_broken/test_autobiographical_narrative_v3.py
  - archived_broken/test_base_v3.py
  - archived_broken/test_batch_predictor_v3.py
  - archived_broken/test_benchmark_suite_v3.py
  - archived_broken/test_bias_detector_v3.py
  - archived_broken/test_biomimetic_safety_bridge_v3.py
  - archived_broken/test_boundary_detector_v3.py
  - archived_broken/test_cbr_engine_v3.py
  - archived_broken/test_certifications_v3.py
  - archived_broken/test_chain_of_thought_v3.py
  - archived_broken/test_client_v3.py
  - archived_broken/test_coherence_v3.py
  - archived_broken/test_communication_v3.py
  - archived_broken/test_compliance_engine_v3.py
  - archived_broken/test_confidence_scoring_v3.py
  - archived_broken/test_confidence_tracker_v3.py
  - archived_broken/test_conflict_resolver_v3.py
  - archived_broken/test_consequentialist_engine_v3.py
  - archived_broken/test_constitutional_validator_100pct.py
  - archived_broken/test_constitutional_validator_v3.py
  - archived_broken/test_constraints_v3.py
  - archived_broken/test_continuous_training_v3.py
  - archived_broken/test_contradiction_detector_v3.py
  - archived_broken/test_controller_old_v3.py
  - archived_broken/test_controller_v3.py
  - archived_broken/test_coordinator_hardened_v3.py
  - archived_broken/test_coordinator_old_unit.py
  - archived_broken/test_coordinator_old_v3.py
  - archived_broken/test_coordinator_v3.py
  - archived_broken/test_core_v3.py
  - archived_broken/test_counterfactual_v3.py
  - archived_broken/test_coverage_report_v3.py
  - archived_broken/test_credential_intel_adw_v3.py
  - archived_broken/test_database_schema_v3.py
  - archived_broken/test_data_collection_v3.py
  - archived_broken/test_data_orchestrator_v3.py
  - archived_broken/test_data_preprocessor_v3.py
  - archived_broken/test_dataset_builder_v3.py
  - archived_broken/test_data_validator_v3.py
  - archived_broken/test_decision_framework_v3.py
  - archived_broken/test_decision_queue_v3.py
  - archived_broken/test_decision_v3.py
  - archived_broken/test_distributed_organism_tools_v3.py
  - archived_broken/test_distributed_trainer_v3.py
  - archived_broken/test_dopamine_hardened_v3.py
  - archived_broken/test_dopamine_system_v3.py
  - archived_broken/test_dp_aggregator_v3.py
  - archived_broken/test_dp_mechanisms_v3.py
  - archived_broken/test_embeddings_v3.py
  - archived_broken/test_emergency_circuit_breaker_v3.py
  - archived_broken/test_engine_v3.py
  - archived_broken/test_enhanced_cognition_tools_v3.py
  - archived_broken/test_enqueue_test_decision_v3.py
  - archived_broken/test_escalation_manager_v3.py
  - archived_broken/test_esgt_subscriber_v3.py
  - archived_broken/test_ethical_guardian_v3.py
  - archived_broken/test_ethical_tool_wrapper_v3.py
  - archived_broken/test_ethics_review_board_v3.py
  - archived_broken/test_evaluator_v3.py
  - archived_broken/test_event_broadcaster_v3.py
  - archived_broken/test_event_collector_v3.py
  - archived_broken/test_event_v3.py
  - archived_broken/test_evidence_collector_v3.py
  - archived_broken/test_example_neuromodulation_standalone_v3.py
  - archived_broken/test_example_neuromodulation_v3.py
  - archived_broken/test_example_predictive_coding_usage_v3.py
  - archived_broken/test_fabric_old_unit.py
  - archived_broken/test_fabric_old_v3.py
  - archived_broken/test_fabric_v3.py
  - archived_broken/test_fase2_coverage_report_v3.py
  - archived_broken/test_feature_tracker_v3.py
  - archived_broken/test_fix_torch_imports_v3.py
  - archived_broken/test_fl_client_v3.py
  - archived_broken/test_fl_coordinator_v3.py
  - archived_broken/test_gap_analyzer_v3.py
  - archived_broken/test_gemini_client_v3.py
  - archived_broken/test_generate_tests_gemini_v3.py
  - archived_broken/test_generate_tests_v3.py
  - archived_broken/test_generate_validation_report_v3.py
  - archived_broken/test_goals_v3.py
  - archived_broken/test_governance_engine_v3.py
  - archived_broken/test_governance_production_server_v3.py
  - archived_broken/test_gpu_trainer_v3.py
  - archived_broken/test_hierarchy_hardened_v3.py
  - archived_broken/test_hitl_interface_v3.py
  - archived_broken/test_hitl_queue_v3.py
  - archived_broken/test_hitl_v3.py
  - archived_broken/test_immune_consciousness_integration.py
  - archived_broken/test_immune_enhancement_tools_v3.py
  - archived_broken/test_industrial_test_generator_v2_v3.py
  - archived_broken/test_industrial_test_generator_v3.py
  - archived_broken/test_industrial_test_generator_v3_v3.py
  - archived_broken/test_inference_engine_v3.py
  - archived_broken/test_integration_100pct.py
  - archived_broken/test_integration_engine_v3.py
  - archived_broken/test_integration_example_v3.py
  - archived_broken/test_introspection_engine_v3.py
  - archived_broken/test_kantian_checker_v3.py
  - archived_broken/test_kantian_v3.py
  - archived_broken/test_kill_switch_v3.py
  - archived_broken/test_knowledge_base_v3.py
  - archived_broken/test_knowledge_v3.py
  - archived_broken/test_kuramoto_v3.py
  - archived_broken/test_layer1_sensory_hardened_v3.py
  - archived_broken/test_layer2_behavioral_hardened_v3.py
  - archived_broken/test_layer3_operational_hardened_v3.py
  - archived_broken/test_layer4_tactical_hardened_v3.py
  - archived_broken/test_layer5_strategic_hardened_v3.py
  - archived_broken/test_layer_base_hardened_v3.py
  - archived_broken/test_layer_trainer_v3.py
  - archived_broken/test_lime_cybersec_v3.py
  - archived_broken/test_logger_v3.py
  - archived_broken/test_mcea_client_v3.py
  - archived_broken/test_mea_bridge.py
  - archived_broken/test_mea_bridge_unit.py
  - archived_broken/test_mea_bridge_v3.py
  - archived_broken/test_memory_buffer_v3.py
  - archived_broken/test_memory_system_v3.py
  - archived_broken/test_metacognition_v3.py
  - archived_broken/test_meta_monitor_v3.py
  - archived_broken/test_metrics_collector_v3.py
  - archived_broken/test_metrics_monitor_v3.py
  - archived_broken/test_metrics_v3.py
  - archived_broken/test_mitigation_v3.py
  - archived_broken/test_mmei_client_v3.py
  - archived_broken/test_model_adapters_v3.py
  - archived_broken/test_model_registry_v3.py
  - archived_broken/test_modulator_base_v3.py
  - archived_broken/test_monitoring_v3.py
  - archived_broken/test_monitor_old_v3.py
  - archived_broken/test_monitor_v3.py
  - archived_broken/test_neuromodulation_controller_v3.py
  - archived_broken/test_norepinephrine_hardened_v3.py
  - archived_broken/test_norepinephrine_system_v3.py
  - archived_broken/test_offensive_arsenal_tools_v3.py
  - archived_broken/test_onnx_exporter_v3.py
  - archived_broken/test_operator_interface_v3.py
  - archived_broken/test_osint_standalone_v3.py
  - archived_broken/test_parse_coverage_audit_v3.py
  - archived_broken/test_phi_proxies_v3.py
  - archived_broken/test_policies_v3.py
  - archived_broken/test_policy_engine_v3.py
  - archived_broken/test_precedent_database_v3.py
  - archived_broken/test_prediction_validator_v3.py
  - archived_broken/test_prefrontal_cortex_v3.py
  - archived_broken/test_principialism_v3.py
  - archived_broken/test_privacy_accountant_v3.py
  - archived_broken/test_profiler_v3.py
  - archived_broken/test_prometheus_exporter_v3.py
  - archived_broken/test_prometheus_metrics_v3.py
  - archived_broken/test_pruner_v3.py
  - archived_broken/test_quantizer_v3.py
  - archived_broken/test_quick_test_v3.py
  - archived_broken/test_rag_system_v3.py
  - archived_broken/test_reasoning_engine_v3.py
  - archived_broken/test_recursive_reasoner_v3.py
  - archived_broken/test_regulations_v3.py
  - archived_broken/test_resource_limiter_v3.py
  - archived_broken/test_risk_assessor_v3.py
  - archived_broken/test_rules_v3.py
  - archived_broken/test_run_api_coverage_v3.py
  - archived_broken/test_run_biomimetic_coverage_v3.py
  - archived_broken/test_run_controller_coverage_v3.py
  - archived_broken/test_run_mea_coverage_v3.py
  - archived_broken/test_run_prefrontal_coverage_v3.py
  - archived_broken/test_run_prometheus_coverage_v3.py
  - archived_broken/test_run_safety_combined_coverage_v3.py
  - archived_broken/test_run_safety_coverage_v3.py
  - archived_broken/test_run_safety_missing_coverage_v3.py
  - archived_broken/test_run_system_coverage_v3.py
  - archived_broken/test_safety_massive_phase_a.py
  - archived_broken/test_safety_v3.py
  - archived_broken/test_salience_detector_v3.py
  - archived_broken/test_salience_scorer_v3.py
  - archived_broken/test_sally_anne_dataset_v3.py
  - archived_broken/test_self_model_v3.py
  - archived_broken/test_self_reflection_v3.py
  - archived_broken/test_sensory_esgt_bridge.py
  - archived_broken/test_sensory_esgt_bridge_v3.py
  - archived_broken/test_serotonin_hardened_v3.py
  - archived_broken/test_serotonin_system_v3.py
  - archived_broken/test_shap_cybersec_v3.py
  - archived_broken/test_simple_v3.py
  - archived_broken/test_skill_learning_controller_v3.py
  - archived_broken/test_social_memory_sqlite_v3.py
  - archived_broken/test_social_memory_v3.py
  - archived_broken/test_sse_server_v3.py
  - archived_broken/test_standalone_server_v3.py
  - archived_broken/test_storage_v3.py
  - archived_broken/test_stress_v3.py
  - archived_broken/test_sync_v3.py
  - archived_broken/test_synthetic_dataset_v3.py
  - archived_broken/test_system_v3.py
  - archived_broken/test_target_profiling_adw_v3.py
  - archived_broken/test_temporal_binding_v3.py
  - archived_broken/test_tom_benchmark_v3.py
  - archived_broken/test_tom_engine_v3.py
  - archived_broken/test_tool_orchestrator_v3.py
  - archived_broken/test_tools_world_class_v3.py
  - archived_broken/test_train_layer1_vae_v3.py
  - archived_broken/test_utilitarian_v3.py
  - archived_broken/test_validate_regra_de_ouro_v3.py
  - archived_broken/test_validate_tig_metrics_v3.py
  - archived_broken/test_validators_v3.py
  - archived_broken/test_vector_db_client_v3.py
  - archived_broken/test_verdict_v3.py
  - archived_broken/test_virtue_ethics_v3.py
  - archived_broken/test_virtue_v3.py
  - archived_v4_tests/test_arousal_integration_v4.py
  - archived_v4_tests/test_base_v4.py
  - archived_v4_tests/test_contradiction_detector_v4.py
  - archived_v4_tests/test_controller_old_v4.py
  - archived_v4_tests/test_controller_v4.py
  - archived_v4_tests/test_coordinator_old_v4.py
  - archived_v4_tests/test_coordinator_v4.py
  - archived_v4_tests/test_esgt_components.py
  - archived_v4_tests/test_euler_vs_rk4_comparison.py
  - archived_v4_tests/test_fabric_old_v4.py
  - archived_v4_tests/test_fabric_v4.py
  - archived_v4_tests/test_goals_v4.py
  - archived_v4_tests/test_immune_e2e_statistics.py
  - archived_v4_tests/test_introspection_engine_v4.py
  - archived_v4_tests/test_kuramoto_v4.py
  - archived_v4_tests/test_meta_monitor_v4.py
  - archived_v4_tests/test_metrics_monitor_v4.py
  - archived_v4_tests/test_monitor_old_v4.py
  - archived_v4_tests/test_monitor_v4.py
  - archived_v4_tests/test_monte_carlo_statistics.py
  - archived_v4_tests/test_recursive_reasoner_v4.py
  - archived_v4_tests/test_robustness_parameter_sweep.py
  - archived_v4_tests/test_run_controller_coverage_v4.py
  - archived_v4_tests/test_salience_detector_v4.py
  - archived_v4_tests/test_simple_v4.py
  - archived_v4_tests/test_stress_v4.py
  - archived_v4_tests/test_sync_v4.py
  - benchmarks/conftest.py
  - benchmarks/__init__.py
  - benchmarks/test_e2e_consciousness_benchmark.py
  - benchmarks/test_esgt_latency_benchmark.py
  - benchmarks/test_mmei_mcea_pipeline_benchmark.py
  - conftest.py
  - e2e/__init__.py
  - e2e/test_pfc_complete.py
  - __init__.py
  - integration/consciousness/test_api_integration_real.py
  - integration/consciousness/test_chaos_engineering.py
  - integration/consciousness/test_circuit_breakers.py
  - integration/consciousness/test_immune_consciousness_integration.py
  - integration/consciousness/test_integration_100pct.py
  - integration/consciousness/test_mea_bridge.py
  - integration/consciousness/test_performance_optimization.py
  - integration/consciousness/test_resilience_final.py
  - integration/consciousness/test_retry_logic.py
  - integration/consciousness/test_sensory_esgt_bridge.py
  - integration/__init__.py
  - integration/test_infrastructure_smoke.py
  - integration/test_pfc_tom_integration.py
  - integration/test_reactive_fabric.py
  - integration/test_system_reactive_fabric.py
  - stress/__init__.py
  - stress/test_concurrency_testing.py
  - stress/test_latency_testing.py
  - stress/test_load_testing.py
  - stress/test_memory_leak_testing.py
  - stress/test_recovery_testing.py
  - test_batch_predictor.py
  - test_benchmark_suite.py
  - test_constitutional_compliance.py
  - test_constitutional_validator_100pct.py
  - test_distributed_trainer.py
  - test_docker_stack.py
  - test_ethical_guardian_100pct.py
  - test_ethical_guardian_backup.py
  - test_gpu_trainer.py
  - test_inference_engine.py
  - test_metrics_export.py
  - test_onnx_exporter.py
  - test_performance_integration.py
  - test_profiler.py
  - test_pruner.py
  - test_quantizer.py
  - unit/compliance/test_regulations_complete.py
  - unit/consciousness/coagulation/test_cascade_95pct.py
  - unit/consciousness/coagulation/test_cascade.py
  - unit/consciousness/episodic_memory/test_core_100pct.py
  - unit/consciousness/episodic_memory/test_episodic_100pct.py
  - unit/consciousness/episodic_memory/test_event_100pct.py
  - unit/consciousness/episodic_memory/test_event_complete.py
  - unit/consciousness/episodic_memory/test_event.py
  - unit/consciousness/episodic_memory/test_memory_buffer.py
  - unit/consciousness/esgt/test_arousal_integration_95pct.py
  - unit/consciousness/esgt/test_coordinator_100pct.py
  - unit/consciousness/esgt/test_coordinator_hardening.py
  - unit/consciousness/esgt/test_esgt_additional.py
  - unit/consciousness/esgt/test_esgt_concurrent.py
  - unit/consciousness/esgt/test_esgt_core_protocol.py
  - unit/consciousness/esgt/test_esgt_degraded.py
  - unit/consciousness/esgt/test_esgt_edge_cases.py
  - unit/consciousness/esgt/test_esgt_final.py
  - unit/consciousness/esgt/test_esgt_node_dropout.py
  - unit/consciousness/esgt/test_esgt.py
  - unit/consciousness/esgt/test_esgt_refractory.py
  - unit/consciousness/esgt/test_esgt_sync_failures.py
  - unit/consciousness/esgt/test_esgt_theory.py
  - unit/consciousness/esgt/test_kuramoto_100pct.py
  - unit/consciousness/esgt/test_kuramoto_final_2_lines.py
  - unit/consciousness/integration_archive_dead_code/test_clients_100pct.py
  - unit/consciousness/integration_archive_dead_code/test_esgt_subscriber_95pct.py
  - unit/consciousness/integration_archive_dead_code/test_mea_bridge_95pct.py
  - unit/consciousness/lrr/test_contradiction_detector_95pct.py
  - unit/consciousness/lrr/test_introspection_engine_95pct.py
  - unit/consciousness/lrr/test_meta_monitor_95pct.py
  - unit/consciousness/lrr/test_recursive_reasoner_100pct.py
  - unit/consciousness/lrr/test_recursive_reasoner.py
  - unit/consciousness/mcea/test_controller_100pct.py
  - unit/consciousness/mcea/test_mcea.py
  - unit/consciousness/mcea/test_stress_100pct.py
  - unit/consciousness/mcea/test_stress_final_17_lines.py
  - unit/consciousness/mcea/test_stress_final_5pct.py
  - unit/consciousness/mcea/test_stress.py
  - unit/consciousness/mcea/test_stress_regression_fix.py
  - unit/consciousness/mea/test_attention_schema_95pct.py
  - unit/consciousness/mea/test_boundary_detector_95pct.py
  - unit/consciousness/mea/test_mea_100pct.py
  - unit/consciousness/mea/test_mea.py
  - unit/consciousness/mea/test_prediction_validator_100pct.py
  - unit/consciousness/mea/test_self_model_95pct.py
  - unit/consciousness/metacognition/test_monitor_100pct.py
  - unit/consciousness/mmei/test_goals_70pct.py
  - unit/consciousness/mmei/test_goals.py
  - unit/consciousness/mmei/test_mmei_coverage_100pct.py
  - unit/consciousness/mmei/test_mmei.py
  - unit/consciousness/neuromodulation/test_all_modulators_hardened.py
  - unit/consciousness/neuromodulation/test_coordinator_hardened.py
  - unit/consciousness/neuromodulation/test_dopamine_hardened.py
  - unit/consciousness/neuromodulation/test_hardened_modulators_100pct.py
  - unit/consciousness/predictive_coding/test_100pct_absolute.py
  - unit/consciousness/predictive_coding/test_all_layers_hardened.py
  - unit/consciousness/predictive_coding/test_coverage_100pct.py
  - unit/consciousness/predictive_coding/test_hierarchy_hardened.py
  - unit/consciousness/predictive_coding/test_layer345_hardened_100pct.py
  - unit/consciousness/predictive_coding/test_layer_base_hardened.py
  - unit/consciousness/predictive_coding/test_layer_hardened_100pct.py
  - unit/consciousness/reactive_fabric/collectors/test_metrics_collector_95pct.py
  - unit/consciousness/reactive_fabric/test_data_orchestrator.py
  - unit/consciousness/reactive_fabric/test_event_collector.py
  - unit/consciousness/reactive_fabric/test_metrics_collector.py
  - unit/consciousness/sandboxing/test_container.py
  - unit/consciousness/sandboxing/test_kill_switch.py
  - unit/consciousness/sandboxing/test_resource_limiter_95pct.py
  - unit/consciousness/sandboxing/test_sandboxing_100pct.py
  - unit/consciousness/test_api_100pct.py
  - unit/consciousness/test_api_missing_lines_100pct.py
  - unit/consciousness/test_api_streaming_100pct.py
  - unit/consciousness/test_autobiographical_95pct.py
  - unit/consciousness/test_autobiographical_narrative_100pct.py
  - unit/consciousness/test_autobiographical_narrative_complete.py
  - unit/consciousness/test_biomimetic_safety_bridge_100pct.py
  - unit/consciousness/test_biomimetic_safety_bridge.py
  - unit/consciousness/test_consciousness_integration.py
  - unit/consciousness/test_edge_cases.py
  - unit/consciousness/test_end_to_end_validation.py
  - unit/consciousness/test_episodic_memory.py
  - unit/consciousness/test_performance.py
  - unit/consciousness/test_prefrontal_cortex_100pct.py
  - unit/consciousness/test_prometheus_metrics_100pct.py
  - unit/consciousness/test_safety_100_final.py
  - unit/consciousness/test_safety_100pct.py
  - unit/consciousness/test_safety_absolute_100.py
  - unit/consciousness/test_safety_final_95pct.py
  - unit/consciousness/test_safety_final_push.py
  - unit/consciousness/test_safety_integration.py
  - unit/consciousness/test_safety_missing_lines.py
  - unit/consciousness/test_safety.py
  - unit/consciousness/test_safety_refactored.py
  - unit/consciousness/test_safety_targeted_phase1.py
  - unit/consciousness/test_safety_targeted_phase2.py
  - unit/consciousness/test_safety_targeted_phase3_final.py
  - unit/consciousness/test_stress_validation.py
  - unit/consciousness/test_system_100pct.py
  - unit/consciousness/test_system_integration.py
  - unit/consciousness/test_temporal_binding_100pct.py
  - unit/consciousness/test_temporal_binding_complete.py
  - unit/consciousness/test_validate_tig_metrics_100pct.py
  - unit/consciousness/tig/test_fabric_100pct.py
  - unit/consciousness/tig/test_fabric_coverage_complete.py
  - unit/consciousness/tig/test_fabric_faith_100pct.py
  - unit/consciousness/tig/test_fabric_final_100pct.py
  - unit/consciousness/tig/test_fabric_final_5_lines.py
  - unit/consciousness/tig/test_fabric_final_9_lines.py
  - unit/consciousness/tig/test_fabric_final_push.py
  - unit/consciousness/tig/test_fabric_hardening.py
  - unit/consciousness/tig/test_fabric_remaining_19.py
  - unit/consciousness/tig/test_sync.py
  - unit/consciousness/tig/test_tig_edge_cases.py
  - unit/consciousness/tig/test_tig.py
  - unit/consciousness/validation/test_metacognition.py
  - unit/consciousness/validation/test_validation_100pct.py
  - unit/__init__.py
  - unit/motor_integridade_processual/infrastructure/test_infrastructure_simple.py
  - unit/test_acetylcholine_hardened_v3.py
  - unit/test_acetylcholine_modulator_targeted.py
  - unit/test_acetylcholine_system_v3.py
  - unit/test_action_plan_v3.py
  - unit/test_advanced_tools_unit.py
  - unit/test_advanced_tools_v3.py
  - unit/test_adw_router_unit.py
  - unit/test_adw_router_v3.py
  - unit/test_agent_templates_unit.py
  - unit/test_agent_templates_v3.py
  - unit/test_aggregation_v3.py
  - unit/test_ai_analyzer_v3.py
  - unit/test_all_services_tools_v3.py
  - unit/test_alternatives_v3.py
  - unit/test_api_routes_unit.py
  - unit/test_api_routes_v3.py
  - unit/test_api_unit.py
  - unit/test_api_v3.py
  - unit/test_arousal_integration_unit.py
  - unit/test_arousal_integration_v3.py
  - unit/test_article_ii_guardian_targeted.py
  - unit/test_article_ii_guardian_v3.py
  - unit/test_article_iii_guardian_targeted.py
  - unit/test_article_iii_guardian_v3.py
  - unit/test_article_iv_guardian_targeted.py
  - unit/test_article_iv_guardian_v3.py
  - unit/test_article_v_guardian_v3.py
  - unit/test_attack_surface_adw_v3.py
  - unit/test_attention_core_v3.py
  - unit/test_attention_schema_v3.py
  - unit/test_audit_infrastructure_v3.py
  - unit/test_audit_trail_v3.py
  - unit/test_audit_v3.py
  - unit/test_autobiographical_narrative_targeted.py
  - unit/test_autobiographical_narrative_v3.py
  - unit/test_base_unit.py
  - unit/test_base_v3.py
  - unit/test_batch_predictor_v3.py
  - unit/test_benchmark_suite_v3.py
  - unit/test_bias_detector_unit.py
  - unit/test_bias_detector_v3.py
  - unit/test_biomimetic_safety_bridge_v3.py
  - unit/test_boundary_detector_targeted.py
  - unit/test_boundary_detector_v3.py
  - unit/test_cbr_engine_v3.py
  - unit/test_certifications_v3.py
  - unit/test_chain_of_thought_v3.py
  - unit/test_client_v3.py
  - unit/test_coagulation_module_targeted.py
  - unit/test_coherence_v3.py
  - unit/test_communication_v3.py
  - unit/test_compliance_engine_v3.py
  - unit/test_confidence_scoring_targeted.py
  - unit/test_confidence_scoring_unit.py
  - unit/test_confidence_scoring_v3.py
  - unit/test_confidence_tracker_v3.py
  - unit/test_conflict_resolver_v3.py
  - unit/test_consciousness_module_targeted.py
  - unit/test_consequentialist_engine_unit.py
  - unit/test_consequentialist_engine_v3.py
  - unit/test_constitutional_validator_unit.py
  - unit/test_constitutional_validator_v3.py
  - unit/test_constraints_v3.py
  - unit/test_continuous_training_v3.py
  - unit/test_contradiction_detector_v3.py
  - unit/test_controller_old_v3.py
  - unit/test_controller_v3.py
  - unit/test_coordinator_hardened_v3.py
  - unit/test_coordinator_old_unit.py
  - unit/test_coordinator_old_v3.py
  - unit/test_coordinator_unit.py
  - unit/test_coordinator_v3.py
  - unit/test_core_v3.py
  - unit/test_counterfactual_v3.py
  - unit/test_coverage_report_unit.py
  - unit/test_coverage_report_v3.py
  - unit/test_credential_intel_adw_v3.py
  - unit/test_database_schema_v3.py
  - unit/test_data_collection_v3.py
  - unit/test_data_orchestrator_coverage.py
  - unit/test_data_orchestrator_unit.py
  - unit/test_data_orchestrator_v3.py
  - unit/test_data_preprocessor_v3.py
  - unit/test_dataset_builder_v3.py
  - unit/test_data_validator_v3.py
  - unit/test_decision_framework_v3.py
  - unit/test_decision_queue_v3.py
  - unit/test_decision_v3.py
  - unit/test_distributed_organism_tools_unit.py
  - unit/test_distributed_organism_tools_v3.py
  - unit/test_distributed_trainer_v3.py
  - unit/test_dopamine_hardened_v3.py
  - unit/test_dopamine_system_v3.py
  - unit/test_dp_aggregator_v3.py
  - unit/test_dp_mechanisms_v3.py
  - unit/test_embeddings_v3.py
  - unit/test_emergency_circuit_breaker_unit.py
  - unit/test_emergency_circuit_breaker_v3.py
  - unit/test_engine_v3.py
  - unit/test_enhanced_cognition_tools_unit.py
  - unit/test_enhanced_cognition_tools_v3.py
  - unit/test_enqueue_test_decision_v3.py
  - unit/test_episodic_memory_core_targeted.py
  - unit/test_escalation_manager_v3.py
  - unit/test_esgt_module_targeted.py
  - unit/test_esgt_spm_module_targeted.py
  - unit/test_esgt_subscriber_v3.py
  - unit/test_ethical_guardian_unit.py
  - unit/test_ethical_guardian_v3.py
  - unit/test_ethical_tool_wrapper_unit.py
  - unit/test_ethical_tool_wrapper_v3.py
  - unit/test_ethics_base_unit.py
  - unit/test_ethics_module_targeted.py
  - unit/test_ethics_review_board_v3.py
  - unit/test_evaluator_v3.py
  - unit/test_event_broadcaster_unit.py
  - unit/test_event_broadcaster_v3.py
  - unit/test_event_collector_coverage.py
  - unit/test_event_collector_unit.py
  - unit/test_event_collector_v3.py
  - unit/test_event_targeted.py
  - unit/test_event_unit.py
  - unit/test_event_v3.py
  - unit/test_evidence_collector_v3.py
  - unit/test_example_neuromodulation_standalone_v3.py
  - unit/test_example_neuromodulation_v3.py
  - unit/test_example_predictive_coding_usage_v3.py
  - unit/test_fabric_old_unit.py
  - unit/test_fabric_old_v3.py
  - unit/test_fabric_v3.py
  - unit/test_fase2_coverage_report_v3.py
  - unit/test_fase_a_batch_14_20.py
  - unit/test_fase_a_batch_21_26.py
  - unit/test_fase_a_batch_27_32.py
  - unit/test_fase_a_batch_33_40.py
  - unit/test_fase_a_batch_41_48.py
  - unit/test_fase_a_batch_49_60_FINAL.py
  - unit/test_fase_a_batch_5_9.py
  - unit/test_fase_b_p0_safety_critical.py
  - unit/test_fase_b_p0_safety_expanded.py
  - unit/test_fase_b_p1_autonomic_analyze.py
  - unit/test_fase_b_p1_simple_modules.py
  - unit/test_fase_b_p2_mip_frameworks.py
  - unit/test_fase_b_p3_final_batch.py
  - unit/test_fase_b_p4_compassion.py
  - unit/test_fase_b_p5_ethics.py
  - unit/test_fase_b_p6_governance.py
  - unit/test_fase_b_p7_fairness.py
  - unit/test_feature_tracker_v3.py
  - unit/test_fix_torch_imports_unit.py
  - unit/test_fix_torch_imports_v3.py
  - unit/test_fl_client_unit.py
  - unit/test_fl_client_v3.py
  - unit/test_fl_coordinator_unit.py
  - unit/test_fl_coordinator_v3.py
  - unit/test_gap_analyzer_v3.py
  - unit/test_gemini_client_unit.py
  - unit/test_gemini_client_v3.py
  - unit/test_generate_tests_gemini_v3.py
  - unit/test_generate_tests_v3.py
  - unit/test_generate_validation_report_v3.py
  - unit/test_goals_v3.py
  - unit/test_governance_engine_targeted.py
  - unit/test_governance_engine_v3.py
  - unit/test_governance_production_server_unit.py
  - unit/test_governance_production_server_v3.py
  - unit/test_governance_sse_standalone_server_targeted.py
  - unit/test_gpu_trainer_v3.py
  - unit/test_hierarchy_hardened_v3.py
  - unit/test_hitl_interface_v3.py
  - unit/test_hitl_queue_v3.py
  - unit/test_hitl_v3.py
  - unit/test_immune_enhancement_tools_targeted.py
  - unit/test_immune_enhancement_tools_unit.py
  - unit/test_immune_enhancement_tools_v3.py
  - unit/test_industrial_test_generator_v2_v3.py
  - unit/test_industrial_test_generator_v3.py
  - unit/test_industrial_test_generator_v3_v3.py
  - unit/test_inference_engine_v3.py
  - unit/test_integration_engine_v3.py
  - unit/test_integration_example_v3.py
  - unit/test_introspection_engine_targeted.py
  - unit/test_introspection_engine_v3.py
  - unit/test_kantian_checker_unit.py
  - unit/test_kantian_checker_v3.py
  - unit/test_kantian_v3.py
  - unit/test_kill_switch_v3.py
  - unit/test_knowledge_base_v3.py
  - unit/test_knowledge_v3.py
  - unit/test_kuramoto_v3.py
  - unit/test_layer1_sensory_hardened_unit.py
  - unit/test_layer1_sensory_hardened_v3.py
  - unit/test_layer1_sensory_targeted.py
  - unit/test_layer2_behavioral_hardened_unit.py
  - unit/test_layer2_behavioral_hardened_v3.py
  - unit/test_layer2_behavioral_targeted.py
  - unit/test_layer3_operational_hardened_unit.py
  - unit/test_layer3_operational_hardened_v3.py
  - unit/test_layer3_operational_targeted.py
  - unit/test_layer4_tactical_hardened_unit.py
  - unit/test_layer4_tactical_hardened_v3.py
  - unit/test_layer4_tactical_targeted.py
  - unit/test_layer5_strategic_hardened_unit.py
  - unit/test_layer5_strategic_hardened_v3.py
  - unit/test_layer_base_hardened_unit.py
  - unit/test_layer_base_hardened_v3.py
  - unit/test_layer_trainer_v3.py
  - unit/test_lime_cybersec_v3.py
  - unit/test_logger_v3.py
  - unit/test_lrr_meta_monitor_targeted.py
  - unit/test_lrr_module_targeted.py
  - unit/test_mcea_client_v3.py
  - unit/test_mcea_module_targeted.py
  - unit/test_mea_bridge_unit.py
  - unit/test_mea_bridge_v3.py
  - unit/test_mea_module_targeted.py
  - unit/test_memory_buffer_v3.py
  - unit/test_memory_system_unit.py
  - unit/test_memory_system_v3.py
  - unit/test_metacognition_unit.py
  - unit/test_metacognition_v3.py
  - unit/test_metacognition_validator_targeted.py
  - unit/test_metacognitive_monitor_targeted.py
  - unit/test_meta_monitor_v3.py
  - unit/test_metrics_collector_coverage.py
  - unit/test_metrics_collector_unit.py
  - unit/test_metrics_collector_v3.py
  - unit/test_metrics_monitor_unit.py
  - unit/test_metrics_monitor_v3.py
  - unit/test_metrics_v3.py
  - unit/test_mip_api_targeted.py
  - unit/test_mip_client_targeted.py
  - unit/test_mitigation_v3.py
  - unit/test_mmei_client_v3.py
  - unit/test_mmei_module_targeted.py
  - unit/test_model_adapters_unit.py
  - unit/test_model_adapters_v3.py
  - unit/test_model_registry_v3.py
  - unit/test_modulator_base_v3.py
  - unit/test_monitoring_v3.py
  - unit/test_monitor_old_v3.py
  - unit/test_monitor_v3.py
  - unit/test_neuromodulation_controller_v3.py
  - unit/test_norepinephrine_hardened_v3.py
  - unit/test_norepinephrine_modulator_targeted.py
  - unit/test_norepinephrine_system_v3.py
  - unit/test_offensive_arsenal_tools_unit.py
  - unit/test_offensive_arsenal_tools_v3.py
  - unit/test_onnx_exporter_v3.py
  - unit/test_operator_interface_v3.py
  - unit/test_osint_standalone_unit.py
  - unit/test_osint_standalone_v3.py
  - unit/test_parse_coverage_audit_unit.py
  - unit/test_parse_coverage_audit_v3.py
  - unit/test_performance_module_targeted.py
  - unit/test_phi_proxies_v3.py
  - unit/test_policies_v3.py
  - unit/test_policy_engine_v3.py
  - unit/test_precedent_database_v3.py
  - unit/test_prediction_validator_targeted.py
  - unit/test_prediction_validator_unit.py
  - unit/test_prediction_validator_v3.py
  - unit/test_prefrontal_cortex_unit.py
  - unit/test_prefrontal_cortex_v3.py
  - unit/test_principialism_v3.py
  - unit/test_privacy_accountant_v3.py
  - unit/test_privacy_module_targeted.py
  - unit/test_profiler_v3.py
  - unit/test_prometheus_exporter_v3.py
  - unit/test_prometheus_metrics_unit.py
  - unit/test_prometheus_metrics_v3.py
  - unit/test_pruner_v3.py
  - unit/test_quantizer_v3.py
  - unit/test_quick_test_v3.py
  - unit/test_rag_system_v3.py
  - unit/test_reasoning_engine_v3.py
  - unit/test_recursive_reasoner_v3.py
  - unit/test_regulations_v3.py
  - unit/test_resource_limiter_targeted.py
  - unit/test_resource_limiter_unit.py
  - unit/test_resource_limiter_v3.py
  - unit/test_risk_assessor_v3.py
  - unit/test_rules_v3.py
  - unit/test_run_api_coverage_unit.py
  - unit/test_run_api_coverage_v3.py
  - unit/test_run_biomimetic_coverage_unit.py
  - unit/test_run_biomimetic_coverage_v3.py
  - unit/test_run_controller_coverage_unit.py
  - unit/test_run_controller_coverage_v3.py
  - unit/test_run_mea_coverage_unit.py
  - unit/test_run_mea_coverage_v3.py
  - unit/test_run_prefrontal_coverage_unit.py
  - unit/test_run_prefrontal_coverage_v3.py
  - unit/test_run_prometheus_coverage_unit.py
  - unit/test_run_prometheus_coverage_v3.py
  - unit/test_run_safety_combined_coverage_unit.py
  - unit/test_run_safety_combined_coverage_v3.py
  - unit/test_run_safety_coverage_unit.py
  - unit/test_run_safety_coverage_v3.py
  - unit/test_run_safety_missing_coverage_unit.py
  - unit/test_run_safety_missing_coverage_v3.py
  - unit/test_run_system_coverage_unit.py
  - unit/test_run_system_coverage_v3.py
  - unit/test_safety_comprehensive.py
  - unit/test_safety_v3.py
  - unit/test_salience_detector_unit.py
  - unit/test_salience_detector_v3.py
  - unit/test_salience_scorer_targeted.py
  - unit/test_salience_scorer_v3.py
  - unit/test_sally_anne_dataset_v3.py
  - unit/test_self_model_targeted.py
  - unit/test_self_model_v3.py
  - unit/test_self_reflection_targeted.py
  - unit/test_self_reflection_v3.py
  - unit/test_sensory_esgt_bridge_v3.py
  - unit/test_serotonin_hardened_v3.py
  - unit/test_serotonin_modulator_targeted.py
  - unit/test_serotonin_system_v3.py
  - unit/test_shap_cybersec_v3.py
  - unit/test_simple_unit.py
  - unit/test_simple_v3.py
  - unit/test_skill_learning_controller_v3.py
  - unit/test_social_memory_sqlite_v3.py
  - unit/test_social_memory_v3.py
  - unit/test_sse_server_v3.py
  - unit/test_standalone_server_unit.py
  - unit/test_standalone_server_v3.py
  - unit/test_storage_v3.py
  - unit/test_stress_unit.py
  - unit/test_stress_v3.py
  - unit/test_sync_v3.py
  - unit/test_synthetic_dataset_v3.py
  - unit/test_system_v3.py
  - unit/test_target_profiling_adw_v3.py
  - unit/test_temporal_binding_targeted.py
  - unit/test_temporal_binding_unit.py
  - unit/test_temporal_binding_v3.py
  - unit/test_tig_module_targeted.py
  - unit/test_tom_benchmark_v3.py
  - unit/test_tom_engine_v3.py
  - unit/test_tool_orchestrator_unit.py
  - unit/test_tool_orchestrator_v3.py
  - unit/test_tools_world_class_v3.py
  - unit/test_train_layer1_vae_v3.py
  - unit/test_utilitarian_v3.py
  - unit/test_validate_regra_de_ouro_unit.py
  - unit/test_validate_regra_de_ouro_v3.py
  - unit/test_validate_tig_metrics_unit.py
  - unit/test_validate_tig_metrics_v3.py
  - unit/test_validation_module_targeted.py
  - unit/test_validators_v3.py
  - unit/test_vector_db_client_v3.py
  - unit/test_verdict_v3.py
  - unit/test_virtue_ethics_v3.py
  - unit/test_virtue_v3.py
```

**Run Tests:**
```bash
cd services/core
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

**Test Fixtures (conftest.py):**
```python
@pytest.fixture(scope="session")
@pytest.fixture
@pytest.fixture
@pytest.fixture
@pytest.fixture
@pytest.fixture
@pytest.fixture
@pytest.fixture(scope="session")
@pytest.fixture(scope="session")
@pytest.fixture
```

---

### dlq_monitor

**Test Files:** 2

**Structure:**
```
  - __init__.py
  - test_constitutional_compliance.py
  - unit/__init__.py
  - unit/test_main_targeted.py
```

**Run Tests:**
```bash
cd services/dlq_monitor
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

---

### eureka

**Test Files:** 16

**Structure:**
```
  - conftest.py
  - __init__.py
  - integration/__init__.py
  - integration/test_sprint2_e2e.py
  - test_constitutional_compliance.py
  - unit/api/__init__.py
  - unit/api/test_ml_metrics.py
  - unit/git_integration/__init__.py
  - unit/git_integration/test_git_models.py
  - unit/__init__.py
  - unit/llm/__init__.py
  - unit/middleware/__init__.py
  - unit/middleware/test_rate_limiter.py
  - unit/orchestration/__init__.py
  - unit/orchestration/test_eureka_orchestrator.py
  - unit/strategies/__init__.py
  - unit/strategies/test_base_strategy.py
  - unit/strategies/test_code_patch_llm.py
  - unit/strategies/test_dependency_upgrade.py
  - unit/test_apv_consumer.py
  - unit/test_ast_grep.py
  - unit/test_breaking_changes_analyzer.py
  - unit/test_coagulation_client.py
  - unit/test_few_shot_database.py
  - unit/test_llm_cost_tracker.py
  - unit/test_patch_models.py
```

**Run Tests:**
```bash
cd services/eureka
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

**Test Fixtures (conftest.py):**
```python
@pytest.fixture
@pytest.fixture
```

---

### maba

**Test Files:** 12

**Structure:**
```
  - conftest.py
  - __init__.py
  - test_api_routes.py
  - test_browser_controller.py
  - test_browser_security_integration.py
  - test_cognitive_map.py
  - test_cognitive_map_sql.py
  - test_constitutional_compliance.py
  - test_dynamic_browser_pool.py
  - test_health.py
  - test_models.py
  - test_robust_element_locator.py
  - test_security_policy.py
  - test_session_manager.py
```

**Run Tests:**
```bash
cd services/maba
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

**Test Fixtures (conftest.py):**
```python
@pytest.fixture
@pytest.fixture
@pytest.fixture
@pytest.fixture
```

---

### nis

**Test Files:** 10

**Structure:**
```
  - conftest.py
  - __init__.py
  - test_anomaly_detector.py
  - test_api_routes.py
  - test_constitutional_compliance.py
  - test_cost_tracker.py
  - test_health.py
  - test_models.py
  - test_narrative_cache.py
  - test_narrative_engine.py
  - test_rate_limiter.py
  - test_system_observer.py
```

**Run Tests:**
```bash
cd services/nis
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

**Test Fixtures (conftest.py):**
```python
@pytest.fixture
@pytest.fixture
@pytest.fixture
```

---

### oraculo

**Test Files:** 15

**Structure:**
```
  - conftest.py
  - e2e/__init__.py
  - __init__.py
  - integration/__init__.py
  - test_constitutional_compliance.py
  - unit/__init__.py
  - unit/test_apv_model.py
  - unit/test_auto_implementer_targeted.py
  - unit/test_code_scanner_targeted.py
  - unit/test_config_targeted.py
  - unit/test_dependency_graph.py
  - unit/test_kafka_publisher.py
  - unit/test_memory_queue_targeted.py
  - unit/test_openai_client_targeted.py
  - unit/test_oraculo_engine.py
  - unit/test_oraculo_targeted.py
  - unit/test_osv_client.py
  - unit/test_relevance_filter.py
  - unit/test_suggestion_generator_targeted.py
  - unit/websocket/__init__.py
  - unit/websocket/test_apv_stream_manager.py
```

**Run Tests:**
```bash
cd services/oraculo
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

**Test Fixtures (conftest.py):**
```python
@pytest.fixture
@pytest.fixture
```

---

### orchestrator

**Test Files:** 2

**Structure:**
```
  - __init__.py
  - test_constitutional_compliance.py
  - test_orchestrator_service.py
```

**Run Tests:**
```bash
cd services/orchestrator
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

---

### penelope

**Test Files:** 19

**Structure:**
```
  - conftest.py
  - __init__.py
  - test_agape_love.py
  - test_api_routes.py
  - test_canary_deployment.py
  - test_chara_joy.py
  - test_circuit_breaker.py
  - test_constitutional_compliance.py
  - test_decision_audit_logger.py
  - test_digital_twin.py
  - test_eirene_peace.py
  - test_enkrateia_self_control.py
  - test_health.py
  - test_human_approval.py
  - test_observability_client.py
  - test_patch_history.py
  - test_pistis_faithfulness.py
  - test_praotes_validator.py
  - test_sophia_engine.py
  - test_tapeinophrosyne_monitor.py
  - test_wisdom_base_client.py
```

**Run Tests:**
```bash
cd services/penelope
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

**Test Fixtures (conftest.py):**
```python
@pytest.fixture
@pytest.fixture
@pytest.fixture
@pytest.fixture
@pytest.fixture
@pytest.fixture
@pytest.fixture
```

---


## Testing Best Practices

### Test Organization
- **Unit Tests**: Test individual functions and classes in isolation
- **Integration Tests**: Test service interactions and API endpoints
- **E2E Tests**: Test complete workflows across multiple services

### Naming Convention
```python
def test_<what_is_being_tested>_<expected_behavior>():
    """Test that <specific scenario> results in <expected outcome>"""
    pass

# Examples:
def test_user_creation_saves_to_database():
    pass

def test_invalid_email_raises_validation_error():
    pass
```

### Test Structure (AAA Pattern)
```python
def test_example():
    # Arrange: Set up test data and conditions
    user = User(name="Test", email="test@example.com")
    
    # Act: Execute the code being tested
    result = user.validate()
    
    # Assert: Verify the expected outcome
    assert result is True
```

### Fixtures and Mocking
```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def sample_user():
    return User(id=1, name="Test User")

def test_with_fixture(sample_user):
    assert sample_user.name == "Test User"

@patch('services.external.api_call')
def test_with_mock(mock_api):
    mock_api.return_value = {"status": "ok"}
    result = my_function()
    assert result == {"status": "ok"}
```

### Running Tests

#### All Tests
```bash
pytest
```

#### Specific Service
```bash
pytest services/eureka/tests/
```

#### Specific File
```bash
pytest services/eureka/tests/test_analysis.py
```

#### Specific Test
```bash
pytest services/eureka/tests/test_analysis.py::test_code_analysis
```

#### With Coverage
```bash
pytest --cov=services --cov-report=html
open htmlcov/index.html
```

#### Parallel Execution
```bash
pytest -n auto  # Uses all CPU cores
```

#### Verbose Output
```bash
pytest -v
```

#### Show Print Statements
```bash
pytest -s
```

---

## Integration Testing

### Service-to-Service Tests
```python
def test_eureka_to_oraculo_integration():
    """Test that Eureka can call Oraculo for risk analysis"""
    # Start both services
    eureka_response = eureka_client.analyze_code(code_sample)
    
    # Verify Oraculo was called
    assert eureka_response.risk_score is not None
```

### Database Tests
```python
@pytest.fixture
def db_session():
    """Provide a database session for tests"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_user_repository(db_session):
    user = User(name="Test")
    db_session.add(user)
    db_session.commit()
    
    found = db_session.query(User).filter_by(name="Test").first()
    assert found is not None
```

### API Endpoint Tests
```python
from fastapi.testclient import TestClient

def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

---

## Coverage Requirements

### Minimum Coverage
- **Unit Tests**: 80% coverage
- **Integration Tests**: 60% coverage
- **Critical Paths**: 100% coverage

### Checking Coverage
```bash
pytest --cov=services --cov-report=term-missing
```

### Coverage Report
```bash
pytest --cov=services --cov-report=html
```

---

## Continuous Integration

### GitHub Actions
Tests run automatically on:
- Pull requests
- Pushes to main branch
- Scheduled daily runs

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## Test Statistics

- **Total Test Files**: 874
- **Services with Tests**: 8

---

**Next Steps:**
- Review [API Reference](../../api-reference/services/)
- Check [Local Setup Guide](../setup/LOCAL_SETUP.md)
