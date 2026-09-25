import json, sys
from pathlib import Path

def evaluate(c):
    reasons=[]
    if c['api_contract_failures']: reasons.append('API contract regression')
    if c['startup_seconds'] > c['max_startup_seconds']: reasons.append('startup SLO breached')
    if c['integration_failures']: reasons.append('integration scenario failed')
    if not c['resource_cleanup_verified']: reasons.append('resource cleanup not verified')
    return {'release_allowed':not reasons,'reasons':reasons}
def run(p): return evaluate(json.loads(Path(p).read_text())['contract'])
if __name__=='__main__':
    if sys.argv[1:]==['--self-test']:
        assert evaluate({'api_contract_failures':0,'startup_seconds':3,'max_startup_seconds':10,'integration_failures':0,'resource_cleanup_verified':True})['release_allowed'];print('systems contract gate: passed')
    else: print(json.dumps(run(sys.argv[1]),indent=2))
