model ExampleFMU
  Modelica.Blocks.Interfaces.RealInput sg annotation(
    Placement(visible = true, transformation(origin = {-114, 2}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-114, 2}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput cg_rate annotation(
    Placement(visible = true, transformation(origin = {110, -2}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-108, 38}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput T_amb annotation(
    Placement(visible = true, transformation(origin = {-114, -38}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-104, -40}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  //Modelica.Blocks.Interfaces.RealOutput T_0;
  parameter Real T_0=0;   // test as  a parameter where the user should be able to change it in realtime.
  Real T(start=T_0);
  Real density;
  parameter Real Cp=1.2552;
  parameter Real dH=91200;
  parameter Real h=0.25;
  Modelica.Blocks.Interfaces.RealOutput Temperature annotation(
    Placement(visible = true, transformation(origin = {108, -48}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {114, -30}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  density=997*sg;
  der (T)=1/(density*Cp)*(dH*cg_rate-h*(T-T_amb));
  Temperature =T;

  annotation(
    uses(Modelica(version = "4.0.0")));
  annotation(
    uses(Modelica(version = "4.0.0")));
end ExampleFMU;
