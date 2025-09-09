    // Example: Generating a clock with a specific period
    module my_clock_generator (
        input wire clk_in,       // Input reference clock (e.g., BUS_CLK)
        output wire clk_out     // Generated clock output
    );

    parameter CLOCK_DIVISOR = 10; // Adjust for desired frequency

    reg [31:0] counter = 0;
    reg clk_out_reg = 0;

    always @(posedge clk_in) begin
        if (counter == (CLOCK_DIVISOR - 1)) begin
            clk_out_reg <= ~clk_out_reg;
            counter <= 0;
        end else begin
            counter <= counter + 1;
        end
    end

    assign clk_out = clk_out_reg;

    endmodule
