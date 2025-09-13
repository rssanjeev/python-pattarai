import requests
import json
from collections import defaultdict

# API endpoints
# GET_URL = "https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=b57c38401d853b750320b54fa513"
# POST_URL = "https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=b57c38401d853b750320b54fa513"

# TEST_URL= "https://candidate.hubteam.com/candidateTest/v3/problem/test-dataset-answer?userKey=b57c38401d853b750320b54fa513"

# Fetch data
response = requests.get(GET_URL)
data = response.json()
users = data["users"]
deals = data["deals"]

# Prepare a mapping for deals owned by each user
deal_owners = {deal["dealId"]: deal["ownerUserId"] for deal in deals}

# Create team mappings
user_teams = defaultdict(set)
for user in users:
    for team in user["teamIds"]:
        user_teams[user["userId"]].add(team)

# Determine users on the same teams
def same_team_users(user_id):
    user_teams_set = user_teams[user_id]
    return {u for u, teams in user_teams.items() if u != user_id and teams & user_teams_set}

# Calculate permissions
results = []
for user in users:
    viewable_deals = set()
    editable_deals = set()

    for deal_id, owner_id in deal_owners.items():
        # Viewing permissions
        if user["viewPermissionLevel"] == "ALL":
            viewable_deals.add(deal_id)
        elif user["viewPermissionLevel"] == "OWNED_ONLY" and owner_id == user["userId"]:
            viewable_deals.add(deal_id)
        elif user["viewPermissionLevel"] == "OWNED_OR_TEAM":
            if owner_id == user["userId"] or owner_id in same_team_users(user["userId"]):
                viewable_deals.add(deal_id)

        # Editing permissions
        if user["editPermissionLevel"] == "ALL":
            editable_deals.add(deal_id)
        elif user["editPermissionLevel"] == "OWNED_ONLY" and owner_id == user["userId"]:
            editable_deals.add(deal_id)
        elif user["editPermissionLevel"] == "OWNED_OR_TEAM":
            if owner_id == user["userId"] or owner_id in same_team_users(user["userId"]):
                editable_deals.add(deal_id)


    results.append({
        'userId': user["userId"],
        'viewableDealIds': list(viewable_deals),
        'editableDealIds': list(editable_deals)
    })

# Send the result
post_data = {'results': results}
#print(json.dumps(post_data))
post_response = requests.post(POST_URL, data=json.dumps(post_data))

# Check if the response was successful
if post_response.status_code == 200:
    print("Results successfully posted.")
else:
    print("Failed to post results:", post_response.text)

#print(data)