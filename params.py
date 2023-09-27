# Original trading parameters
initial_params = {
    'stop_loss': 1.0,
    'take_profit': 2.0,
    'lot_size': 0.1
}

# New parameters as a string
new_params_code = """
stop_loss = 0.5
take_profit = 1.5
lot_size = 0.2
"""

print(initial_params)
# Use exec to apply the new parameters
exec(new_params_code)

# The trading parameters are now updated
print(initial_params)
