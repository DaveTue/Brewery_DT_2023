model ExampleFMU
  Modelica.Blocks.Interfaces.RealInput sg annotation(
    Placement(visible = true, transformation(origin = {-114, 2}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-114, 2}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput cg_rate annotation(
    Placement(visible = true, transformation(origin = {-108, 42}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-108, 38}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput T_pump annotation(
    Placement(visible = true, transformation(origin = {-114, -38}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-104, -40}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput T_amb annotation(
    Placement(visible = true, transformation(origin = {-118, -76}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-104, -40}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput pump_state annotation(
    Placement(visible = true, transformation(origin = {-154, -54}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-104, -40}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));

   Modelica.Blocks.Interfaces.RealInput Volume annotation(
    Placement(visible = true, transformation(origin = {-120, 86}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-104, -40}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));

  //Modelica.Blocks.Interfaces.RealOutput T_0;
  parameter Real T_0=0;   // test as  a parameter where the user should be able to change it in realtime.
  Real T(start=T_0);
  Real density;
  parameter Real Cp=1.2552;
  parameter Real dH=91200;
  parameter Real h=322.89;
  parameter Real A_coil=0.1817;
  parameter Real h_amb=42.9315;
  parameter Real A_ferm=0.7540;
  
  Real Vol_meters;
  
  Modelica.Blocks.Interfaces.RealOutput Temperature annotation(
    Placement(visible = true, transformation(origin = {108, -48}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {114, -30}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput Q_beer annotation(
    Placement(visible = true, transformation(origin = {106, 48}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {114, -30}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));

equation
  density=997*sg;
  Vol_meters=Volume/1000;
  der (T)=1/(density*Cp*Vol_meters)*(-dH*cg_rate*Vol_meters-pump_state*h*(T-T_pump)-h_amb*A_ferm*(T-T_amb));
  Temperature =T;
  Q_beer=density*Cp*Vol_meters*der(T);

  annotation(
    uses(Modelica(version = "4.0.0")));
  annotation(
    uses(Modelica(version = "4.0.0")));
end ExampleFMU;
