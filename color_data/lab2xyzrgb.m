%Assumes local file named v_to_cielab.csv
v_to_cielab=csvread('v_to_cielab.csv');
V=v_to_cielab(:,1);
lab=v_to_cielab(:,2:4);
xyz=lab2xyz(lab);
rgb=xyz2rgb(xyz);
rgb256=255.0*rgb;

xyz_table=[V xyz];
rgb256_table=[V rgb256];

csvwrite('v_to_ciexyz.csv',xyz_table);
csvwrite('v_to_rgb.csv',rgb256_table);
