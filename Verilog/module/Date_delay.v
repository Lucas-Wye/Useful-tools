module
    Data_delay
    # (
        parameter WIDTH = 1,
        parameter DELAY = 3  // cycle
    )
    (
        input clk,
        input [WIDTH-1:0] data_in,
        output [WIDTH-1:0] data_out
    );

reg [WIDTH*DELAY-1:0] data_r;
always @ (posedge clk) begin
    data_r <= {data_r[WIDTH*(DELAY-1)-1:0],data_in};
end

assign data_out = data_r[WIDTH*DELAY-1:WIDTH*DELAY-WIDTH];

endmodule
