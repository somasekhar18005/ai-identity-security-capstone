from nemoguardrails import RailsConfig, LLMRails


config = RailsConfig.from_path("./config")
rails = LLMRails(config)


attacks = {
    "F-01": "PASTE PROJECT 3 F-01 PAYLOAD/OUTPUT HERE",
    "F-02": "PASTE PROJECT 3 F-02 PAYLOAD/OUTPUT HERE",
    "F-03": "PASTE PROJECT 3 F-03 PAYLOAD/OUTPUT HERE",
    "F-04": "PASTE PROJECT 3 F-04 PAYLOAD/OUTPUT HERE",
    "F-05": "PASTE PROJECT 3 F-05 PAYLOAD/OUTPUT HERE",
}


print("=" * 70)
print("PROJECT 4 - TASK 1")
print("PROJECT 3 ATTACK REPLAY THROUGH OUTPUT GUARDRAIL")
print("=" * 70)

for attack_id, attack_output in attacks.items():

    messages = [
        {
            "role": "user",
            "content": f"Replay attack {attack_id}"
        },
        {
            "role": "assistant",
            "content": attack_output
        }
    ]

    result = rails.check(messages)

    print(f"\n{attack_id}")
    print("-" * 40)
    print(f"Status : {result.status}")
    print(f"Output : {result.content}")

print("\n" + "=" * 70)