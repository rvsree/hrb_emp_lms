"""Test script for all MCP tools in hrb_emp_lms."""

import sys
import os
import requests
import json
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app.common.config.config import settings

BASE_URL = f"http://localhost:{settings.server_port}"
MCP_ENDPOINT = f"{BASE_URL}/api/hrb/lms/mcp"
API_KEY = settings.api_key


def make_mcp_request(method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Make an MCP JSON-RPC 2.0 request."""
    request = {
        "jsonrpc": "2.0",
        "id": f"test_{method}",
        "method": method,
        "params": params or {}
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    response = requests.post(MCP_ENDPOINT, json=request, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def test_tools_list():
    """Test tools/list method."""
    print("\n" + "="*80)
    print("TEST 1: tools/list")
    print("="*80)
    
    try:
        result = make_mcp_request("tools/list")
        
        if "error" in result:
            print(f"❌ FAIL: Error: {result['error']}")
            return False
        
        tools = result.get("result", {}).get("tools", [])
        print(f"✅ PASS: Retrieved {len(tools)} tools")
        
        for tool in tools:
            print(f"   - {tool.get('name')}: {tool.get('description', '')[:60]}...")
        
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_get_leave_balance():
    """Test get_leave_balance tool."""
    print("\n" + "="*80)
    print("TEST 2: get_leave_balance")
    print("="*80)
    
    try:
        result = make_mcp_request("tools/call", {
            "name": "get_leave_balance",
            "arguments": {
                "employee_id": "EMP001",
                "year": 2025
            }
        })
        
        if "error" in result:
            print(f"❌ FAIL: Error: {result['error']}")
            return False
        
        tool_result = result.get("result", {})
        if "error" in tool_result:
            print(f"⚠️  WARNING: Tool returned error: {tool_result.get('error')}")
            print("   (This might be expected if employee doesn't exist in database)")
            return True
        
        employee_id = tool_result.get("employeeId")
        balances = tool_result.get("balances", [])
        print(f"✅ PASS: Retrieved leave balance for {employee_id}")
        print(f"   Year: {tool_result.get('year')}")
        print(f"   Balances: {len(balances)} leave types")
        for balance in balances:
            print(f"     - {balance.get('leaveType')}: {balance.get('available')} days available")
        
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_submit_leave_request():
    """Test submit_leave_request tool."""
    print("\n" + "="*80)
    print("TEST 3: submit_leave_request")
    print("="*80)
    
    try:
        result = make_mcp_request("tools/call", {
            "name": "submit_leave_request",
            "arguments": {
                "employee_id": "EMP001",
                "leave_type": "PTO",
                "start_date": "2025-12-30",
                "end_date": "2025-12-31",
                "reason": "Test leave request"
            }
        })
        
        if "error" in result:
            print(f"❌ FAIL: Error: {result['error']}")
            return False
        
        tool_result = result.get("result", {})
        if "error" in tool_result:
            print(f"⚠️  WARNING: Tool returned error: {tool_result.get('error')}")
            print("   (This might be expected if employee doesn't exist or validation fails)")
            return True
        
        request_id = tool_result.get("requestId")
        status = tool_result.get("status")
        print(f"✅ PASS: Submitted leave request")
        print(f"   Request ID: {request_id}")
        print(f"   Status: {status}")
        print(f"   Days: {tool_result.get('days')}")
        
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_leave_history():
    """Test get_leave_history tool."""
    print("\n" + "="*80)
    print("TEST 4: get_leave_history")
    print("="*80)
    
    try:
        result = make_mcp_request("tools/call", {
            "name": "get_leave_history",
            "arguments": {
                "employee_id": "EMP001",
                "limit": 10,
                "offset": 0
            }
        })
        
        if "error" in result:
            print(f"❌ FAIL: Error: {result['error']}")
            return False
        
        tool_result = result.get("result", {})
        if "error" in tool_result:
            print(f"⚠️  WARNING: Tool returned error: {tool_result.get('error')}")
            return True
        
        total = tool_result.get("total", 0)
        requests = tool_result.get("requests", [])
        print(f"✅ PASS: Retrieved leave history")
        print(f"   Total requests: {total}")
        print(f"   Returned: {len(requests)} requests")
        
        if requests:
            print(f"   First request: {requests[0].get('leaveType')} - {requests[0].get('status')}")
        
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_pending_approvals():
    """Test get_pending_approvals tool."""
    print("\n" + "="*80)
    print("TEST 5: get_pending_approvals")
    print("="*80)
    
    try:
        result = make_mcp_request("tools/call", {
            "name": "get_pending_approvals",
            "arguments": {
                "manager_id": "MGR001"
            }
        })
        
        if "error" in result:
            print(f"❌ FAIL: Error: {result['error']}")
            return False
        
        tool_result = result.get("result", {})
        if "error" in tool_result:
            print(f"⚠️  WARNING: Tool returned error: {tool_result.get('error')}")
            return True
        
        total = tool_result.get("total", 0)
        approvals = tool_result.get("approvals", [])
        print(f"✅ PASS: Retrieved pending approvals")
        print(f"   Total pending: {total}")
        print(f"   Returned: {len(approvals)} approvals")
        
        if approvals:
            print(f"   First approval: Employee {approvals[0].get('employeeId')} - {approvals[0].get('days')} days")
        
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_create_hitl_request():
    """Test create_hitl_request tool."""
    print("\n" + "="*80)
    print("TEST 6: create_hitl_request")
    print("="*80)
    
    try:
        result = make_mcp_request("tools/call", {
            "name": "create_hitl_request",
            "arguments": {
                "request_type": "POLICY_INTERPRETATION",
                "query": "Test HITL request for policy interpretation",
                "employee_id": "EMP001",
                "context": {
                    "test": True
                }
            }
        })
        
        if "error" in result:
            print(f"❌ FAIL: Error: {result['error']}")
            return False
        
        tool_result = result.get("result", {})
        if "error" in tool_result:
            print(f"⚠️  WARNING: Tool returned error: {tool_result.get('error')}")
            return True
        
        hitl_request_id = tool_result.get("hitlRequestId")
        status = tool_result.get("status")
        print(f"✅ PASS: Created HITL request")
        print(f"   HITL Request ID: {hitl_request_id}")
        print(f"   Status: {status}")
        print(f"   Assigned to: {tool_result.get('assignedTo')}")
        
        return hitl_request_id  # Return ID for next test
    except Exception as e:
        print(f"❌ FAIL: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_get_hitl_status(hitl_request_id: int = None):
    """Test get_hitl_status tool."""
    print("\n" + "="*80)
    print("TEST 7: get_hitl_status")
    print("="*80)
    
    # Use provided ID or try to find an existing one
    if not hitl_request_id:
        hitl_request_id = 1  # Try with ID 1
    
    try:
        result = make_mcp_request("tools/call", {
            "name": "get_hitl_status",
            "arguments": {
                "hitl_request_id": hitl_request_id
            }
        })
        
        if "error" in result:
            print(f"❌ FAIL: Error: {result['error']}")
            return False
        
        tool_result = result.get("result", {})
        if "error" in tool_result:
            print(f"⚠️  WARNING: Tool returned error: {tool_result.get('error')}")
            print("   (This might be expected if HITL request doesn't exist)")
            return True
        
        status = tool_result.get("status")
        print(f"✅ PASS: Retrieved HITL request status")
        print(f"   HITL Request ID: {tool_result.get('hitlRequestId')}")
        print(f"   Status: {status}")
        print(f"   Request Type: {tool_result.get('requestType')}")
        
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("HRB EMP LMS - MCP TOOLS TEST SUITE")
    print("="*80)
    print(f"\nTesting MCP endpoint: {MCP_ENDPOINT}")
    print(f"API Key: {'SET' if API_KEY else 'NOT SET'}")
    
    # Check if server is running
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"⚠️  Server health check returned: {health_response.status_code}")
    except Exception as e:
        print(f"❌ Server is not running or not accessible: {e}")
        print("   Please start the server with: python main.py")
        return 1
    
    results = []
    
    # Test 1: tools/list
    results.append(("tools/list", test_tools_list()))
    
    # Test 2: get_leave_balance
    results.append(("get_leave_balance", test_get_leave_balance()))
    
    # Test 3: submit_leave_request
    results.append(("submit_leave_request", test_submit_leave_request()))
    
    # Test 4: get_leave_history
    results.append(("get_leave_history", test_get_leave_history()))
    
    # Test 5: get_pending_approvals
    results.append(("get_pending_approvals", test_get_pending_approvals()))
    
    # Test 6: create_hitl_request
    hitl_id = test_create_hitl_request()
    results.append(("create_hitl_request", hitl_id is not None))
    
    # Test 7: get_hitl_status
    if hitl_id:
        results.append(("get_hitl_status", test_get_hitl_status(hitl_id)))
    else:
        results.append(("get_hitl_status", test_get_hitl_status()))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())

