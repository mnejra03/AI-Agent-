def agent_loop():
    while True:
        item = get_request()
        if not item:
            time.sleep(0.5)
            continue

        request_id, data = item

        risk = agent.think(agent.sense(data))
        decision = agent.act(risk, data)
        explanation = agent.explain(data, decision)

        save_result(request_id, {
            "risk": risk,
            "decision": decision,
            "explanation": explanation
        })
