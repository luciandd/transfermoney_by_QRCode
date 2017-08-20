API_VERSION = 'v1.0'

# Authentication
LOGIN_URL = API_VERSION + "/agent/oauth/token"
LOGOUT_URL = API_VERSION + "/oauth/token/revoke"

#Service
SERVICE_LIST_URL="payment/" + API_VERSION + "/admin/services"

#SOF
SOF_TYPES_URL="payment/" + API_VERSION + "/sof-types"

#AGENT
GET_AGENT_SOF_ID_URL="agent/" + API_VERSION + "/agents/{agentId}/balances/{currency}"
