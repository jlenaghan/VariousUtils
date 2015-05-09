#   Calculate Descriptive Statistics: min, max, median, mode, deciles

sort -n $* |
awk 'BEGIN { max = -999999999; min = 999999999; }
    {   # Accumulate basic data
        count[$1]++;
        item[++n] = $1;
        if ($1 > max) max = $1;
        if ($1 < min) min = $1;
    }
END {   # Print Descriptive Statistics
        printf("# Count = %d\n", n);
        printf("# Min = %d\n", min);
        decile = 1;
        for (decile = 10; decile < 100; decile += 10)
        {
            idx = int((decile * n) / 100) + 1;
            printf("# %d%% decile = %d\n", decile, item[idx]);
            if (decile == 50)
                median = item[idx];
        }
        printf("# Max = %d\n", max);

        printf("# Median = %d\n", median);
        for (i in count)
        {
            if (count[i] > count[mode])
                mode = i;
        }
        printf("# Mode = %d\n", mode);
    }'
