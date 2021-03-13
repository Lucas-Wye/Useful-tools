module D_EF
       #(
           parameter N_WIDTH = 13,
           parameter N_POINT = 16,
           parameter LOG_N = 4,
           parameter PARAM_K = 26,
           parameter PARAM_M = 8736,
           parameter PARAM_Q = 7681
       )(
           input clk,
           input wire [N_WIDTH-1:0]D,
           output reg [N_WIDTH-1:0]Q
       );

always @(posedge clk)
begin
    Q <= D;
end
endmodule
