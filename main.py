import json
from sast_orchestrator import SASTOrchestrator
from results_aggregator import ResultsAggregator
from issue_tracker import IssueTracker

def load_config(config_path):
    with open(config_path) as f:
        return json.load(f)

def main():
    config = load_config('tools_config.json')
    
    # Initialize components
    orchestrator = SASTOrchestrator('https://github.com/your/repo', config)
    raw_results = orchestrator.run_scans()
    
    aggregator = ResultsAggregator(raw_results)
    normalized_results = aggregator.normalize_results()
    
    tracker = IssueTracker(config.get('issue_tracker', {}))
    tracker.create_issues(normalized_results)

if __name__ == "__main__":
    main() 