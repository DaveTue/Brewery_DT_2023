from OMSimulator import OMSimulator, Types
import json

oms = OMSimulator()
model, status = oms.importFile("s1s2.ssp")
print(Types.Status(status))

oms.setResultFile(model, "results.csv", bufferSize=10)

oms.instantiate(model)
oms.setReal('s1s2.Root.Reaction_model.Temperature', 299.15)
oms.setReal('s1s2.Root.Reaction_model.grams_yeast', 11.5)
oms.setReal('s1s2.Root.Reaction_model.sg_0', 1.054)
oms.setReal('s1s2.Root.Reaction_model.batch_volume', 20)
oms.setReal('s1s2.Root.control_model.T_set', 22)
oms.setReal('s1s2.Root.control_model.T_sensor', 19)

oms.initialize(model)
oms.simulate(model)

data = {"command": int(oms.getReal('s1s2.Root.control_model.control_signal')[0])}
with open('control.json', 'w') as f:
    json.dump(data, f)

oms.terminate(model)
oms.delete(model)