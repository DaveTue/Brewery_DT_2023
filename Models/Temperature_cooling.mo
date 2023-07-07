model ExampleFMU
  Modelica.Blocks.Interfaces.RealInput T_amb annotation(
    Placement(visible = true, transformation(origin = {-162, -86}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-102, -32}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput radious_bucket annotation(
    Placement(visible = true, transformation(origin = {-122, 54}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-102, -32}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput pump_state annotation(
    Placement(visible = true, transformation(origin = {-126, -12}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-104, -40}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));

  Modelica.Blocks.Interfaces.RealInput heigh_bucket annotation(
    Placement(visible = true, transformation(origin = {-120, 24}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-102, -32}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput icepack_heigh annotation(
    Placement(visible = true, transformation(origin = {-170, 82}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-102, -32}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput icepack_long annotation(
    Placement(visible = true, transformation(origin = {-198, 56}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-102, -32}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput icepack_thick annotation(
    Placement(visible = true, transformation(origin = {-124, 90}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-102, -32}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput Q_beer annotation(
    Placement(visible = true, transformation(origin = {-126, -42}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-102, -32}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));

//Modelica.Blocks.Interfaces.RealInput density annotation(
  //Placement(visible = true, transformation(origin = {-114, 2}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-118, 52}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  //Modelica.Blocks.Interfaces.RealInput cg_rate annotation(
  //  Placement(visible = true, transformation(origin = {110, -2}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, -2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  //Modelica.Blocks.Interfaces.RealOutput T_0;
  parameter Real T_0=0;
  parameter Real T_0_icepack=-9.4;
  Real T(start=T_0);
  Real T_icepack(start=T_0_icepack);
  //Real T_h;
  Real m_H2O;
  Real A_icepack;
  Real A_free;
  Real A_bucket_wall;
  Real Q_h2o;
  parameter Real Cp=4184;
  parameter Real H2O_massflow=0.09693;   //m3/s
  parameter Real H2O_density=997;
  //kg/m3
  parameter Real h_icepack=115.0422;
  parameter Real h_bucket = 29.1252;
  parameter Real h_air=55;
  parameter Real m_icepack=0.8144;
  parameter Real Cp_icepack=5702.4;
  //parameter Real dH=91200;
  //parameter Real h=8;
  final constant Real pi=2*Modelica.Math.asin(1.0);
  Modelica.Blocks.Interfaces.RealOutput T_cool annotation(
    Placement(visible = true, transformation(origin = {124, 52}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-102, -32}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));

equation
  m_H2O=radious_bucket^2*heigh_bucket*pi*H2O_density;
  A_icepack=2*(icepack_heigh*icepack_long+icepack_thick*icepack_heigh+icepack_long*icepack_thick);
  A_free=pi*radious_bucket^2;
  A_bucket_wall=2*pi*radious_bucket*heigh_bucket;
//der (T)=1/(m_H2O*Cp)*(-H2O_massflow*Cp*(T-T_h)+h_air*A_free*(T-T_amb)+h_bucket*A_bucket_wall*(T-T_amb)+h_icepack*A_icepack*(T-T_icepack));
  der (T)=1/(m_H2O*Cp)*(-pump_state*Q_beer+h_air*A_free*(T-T_amb)+h_bucket*A_bucket_wall*(T-T_amb)+h_icepack*A_icepack*(T-T_icepack));
  T_cool=T;
  Q_h2o=m_H2O*Cp*der(T);
  der(T_icepack)=Q_h2o/(m_icepack*Cp_icepack);
  

  annotation(
    uses(Modelica(version = "4.0.0")));
  annotation(
    uses(Modelica(version = "4.0.0")));
end ExampleFMU;
