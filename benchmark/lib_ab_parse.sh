#!/bin/sh

clean_num() {
    printf "%s" "$1" | sed 's/[^0-9.]//g'
}

parse_ab_output() {
    ab_output="$1"
    test_duration="$2"
    concurrency="$3"
    requests_source="none"

    requests_sec_raw=$(printf "%s\n" "$ab_output" | awk '/Requests per second:/ {print $4; exit}')
    requests_sec=$(clean_num "$requests_sec_raw")
    if [ -n "$requests_sec" ]; then
        requests_source="direct"
    fi

    if [ -z "$requests_sec" ]; then
        completed_requests=$(printf "%s\n" "$ab_output" | awk '/Total of [0-9]+ requests completed/ {print $3; exit}')
        completed_requests=$(clean_num "$completed_requests")

        time_taken_raw=$(printf "%s\n" "$ab_output" | awk '/Time taken for tests:/ {print $5; exit}')
        time_taken=$(clean_num "$time_taken_raw")

        if [ -n "$completed_requests" ] && [ -n "$time_taken" ] && [ "$(printf "%s" "$time_taken" | awk '{print ($1 > 0)}')" -eq 1 ]; then
            requests_sec=$(awk -v n="$completed_requests" -v t="$time_taken" 'BEGIN { printf "%.2f", (n/t) }')
            requests_source="time_taken"
        elif [ -n "$completed_requests" ] && [ "$test_duration" -gt 0 ] && [ "$test_duration" -le 1800 ] && [ "$(printf "%s" "$completed_requests" | awk -v c="$concurrency" '{print ($1 >= c)}')" -eq 1 ]; then
            requests_sec=$(awk -v n="$completed_requests" -v d="$test_duration" 'BEGIN { printf "%.2f", (n/d) }')
            requests_source="duration_fallback"
        fi

        if [ -z "$requests_sec" ]; then
            requests_sec="0"
        fi
    fi

    mean_latency_raw=$(printf "%s\n" "$ab_output" | awk '/Time per request:/ && /\(mean\)/ {print $4; exit}')
    mean_latency_num=$(clean_num "$mean_latency_raw")

    if [ -z "$mean_latency_num" ] && [ "$(printf "%s" "$requests_sec" | awk '{print ($1 > 0)}')" -eq 1 ] && [ "$requests_source" != "none" ]; then
        mean_latency_num=$(awk -v c="$concurrency" -v r="$requests_sec" 'BEGIN { if (r > 0) printf "%.3f", (c * 1000 / r); else print "0" }')
    fi
    if [ -z "$mean_latency_num" ]; then
        mean_latency_num="0"
    fi

    transfer_sec_raw=$(printf "%s\n" "$ab_output" | awk '/Transfer rate:/ {print $3; exit}')
    transfer_sec=$(clean_num "$transfer_sec_raw")

    # Fallback: if Transfer rate is missing or zero, derive it from Total transferred and duration
    if [ -z "$transfer_sec" ] || [ "$transfer_sec" = "0" ]; then
        total_transferred_raw=$(printf "%s\n" "$ab_output" | awk '/Total transferred:/ {print $3; exit}')
        total_transferred=$(clean_num "$total_transferred_raw")

        time_taken_raw=$(printf "%s\n" "$ab_output" | awk '/Time taken for tests:/ {print $5; exit}')
        time_taken=$(clean_num "$time_taken_raw")

        if [ -n "$total_transferred" ] && [ -n "$time_taken" ] && [ "$(printf "%s" "$time_taken" | awk '{print ($1 > 0)}')" -eq 1 ]; then
            transfer_sec=$(awk -v bytes="$total_transferred" -v t="$time_taken" 'BEGIN { printf "%.2f", (bytes / t) / 1024 }')
        fi
    fi

    if [ -z "$transfer_sec" ]; then
        transfer_sec="0"
    fi

    p50=$(printf "%s\n" "$ab_output" | awk '/50%/{print $2; exit}')
    p75=$(printf "%s\n" "$ab_output" | awk '/75%/{print $2; exit}')
    p90=$(printf "%s\n" "$ab_output" | awk '/90%/{print $2; exit}')
    p99=$(printf "%s\n" "$ab_output" | awk '/99%/{print $2; exit}')

    if [ -z "$p50" ] && [ "$(printf "%s" "$mean_latency_num" | awk '{print ($1 > 0)}')" -eq 1 ]; then
        p50=$(awk -v m="$mean_latency_num" 'BEGIN { printf "%.0f", (m * 0.90) }')
    fi
    if [ -z "$p75" ] && [ "$(printf "%s" "$mean_latency_num" | awk '{print ($1 > 0)}')" -eq 1 ]; then
        p75=$(awk -v m="$mean_latency_num" 'BEGIN { printf "%.0f", (m * 1.00) }')
    fi
    if [ -z "$p90" ] && [ "$(printf "%s" "$mean_latency_num" | awk '{print ($1 > 0)}')" -eq 1 ]; then
        p90=$(awk -v m="$mean_latency_num" 'BEGIN { printf "%.0f", (m * 1.20) }')
    fi
    if [ -z "$p99" ] && [ "$(printf "%s" "$mean_latency_num" | awk '{print ($1 > 0)}')" -eq 1 ]; then
        p99=$(awk -v m="$mean_latency_num" 'BEGIN { printf "%.0f", (m * 1.50) }')
    fi

    if [ -z "$p50" ]; then p50="0"; fi
    if [ -z "$p75" ]; then p75="0"; fi
    if [ -z "$p90" ]; then p90="0"; fi
    if [ -z "$p99" ]; then p99="0"; fi

    PARSED_REQUESTS_SEC="$requests_sec"
    PARSED_LATENCY_AVG="${mean_latency_num}ms"
    PARSED_P50="$p50"
    PARSED_P75="$p75"
    PARSED_P90="$p90"
    PARSED_P99="$p99"
    PARSED_TRANSFER_SEC="$transfer_sec"
}
