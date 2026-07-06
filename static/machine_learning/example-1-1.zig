const std = @import("std");

pub fn main() !void {
    // Main function mostly does set up and runs the optimizer on the included arbitary function
    // For the most part, you can ignore it.
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();

    const allocator = arena.allocator();

    std.debug.print("Optimized arbFunc1: {any}\n", .{optimize(
        allocator,
        arbitaryFunction1,
        7,
    )});
}

pub fn arbitaryFunction1(inputs: []const i8) i8 {
    // this is just f(x,y,z...) = -(x^2) -(y^2) -(z^2)...
    var output: i8 = 0;
    for (inputs) |value| {
        output = output - ((value - 1) * (value - 1));
    }
    return output;
}

const arbFunc = *const fn (inputs: []i8) i8;
pub fn optimize(allocator: std.mem.Allocator, func: arbFunc, variableCount: u8) ![]i8 {

    // We set our best point to be all 0s at the start.
    var bestPoint = try allocator.alloc(i8, variableCount);
    @memset(bestPoint, 0);

    // Then we compute our best value
    var bestValue = func(bestPoint);

    // We can assume we haven't hit a global max by luck
    var possibleGlobalMax = false;

    // This will be the array for the points we test out
    var speculativePoint = try allocator.alloc(i8, variableCount);
    defer allocator.free(speculativePoint);
    @memset(speculativePoint, 0);

    // We start our search with a small window, i.e. searching plus/minus 1 for each axis
    var searchWindow: i8 = 1;
    while (!possibleGlobalMax) {
        var localMax = true;
        @memcpy(bestPoint, speculativePoint);

        for (0..variableCount) |i| {
            // This is to search from plus/minus searchWindow rather than just plus searchWindow
            var j: i8 = -searchWindow;
            while (j < searchWindow) {
                // Add the amount and compute the new value.
                std.debug.print("{d}\n", .{j});
                speculativePoint[i] = speculativePoint[i] + j;
                std.debug.print("{any}\n", .{speculativePoint});
                const speculativeValue = func(speculativePoint);

                // If the new value is better, we set it as the best value
                if (speculativeValue > bestValue) {
                    bestPoint[i] = bestPoint[i] + j;
                    bestValue = speculativeValue;
                    localMax = false;
                } else {
                    // Reverts the change if the new value is not better
                    speculativePoint[i] = speculativePoint[i] - j;
                }
                j = j + 1;
            }
        }

        std.debug.print("{any}\n", .{bestValue});

        // If we are confident that we are at a local max, try expanding the search window
        // This trying to avoid being trapped at the local max, but likely does not actually solve the issue.
        if (localMax) {
            searchWindow = searchWindow + 1;
        }

        if (searchWindow > 3) {
            possibleGlobalMax = true;
        }
    }
    return bestPoint;
}
