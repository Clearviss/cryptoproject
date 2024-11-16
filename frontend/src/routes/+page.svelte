<script lang="ts">
    import { onMount } from "svelte";

    let portfolio: any[] = [];
    let totalValue = 0;

    onMount(async () => {
        const response = await fetch("http://127.0.0.1:5000/portfolio");
        const data = await response.json();
        portfolio = data.portfolio;
        totalValue = data.total_value_usdt;

        const interval = setInterval(async () => {
            const response = await fetch("http://127.0.0.1:5000/portfolio");
            const data = await response.json();
            portfolio = data.portfolio;
            totalValue = data.total_value_usdt;
        }, 10000);
    });

    console.log(portfolio);
</script>

<main>
    <div class="relative overflow-x-auto">
        <div
            class="p-4 pb-4 bg-white dark:bg-gray-900 text-white text-center text-2xl"
        >
            Łączna wartość klubu: {totalValue.toFixed()} USDT
        </div>
        <table
            class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400"
        >
            <thead
                class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
            >
                <tr>
                    <th scope="col" class="px-6 py-3"> Symbol </th>
                    <th scope="col" class="px-6 py-3"> Cena </th>
                    <th scope="col" class="px-6 py-3"> Ilość </th>
                    <th scope="col" class="px-6 py-3"> Wartość </th>
                </tr>
            </thead>
            <tbody>
                {#each portfolio as item}
                    <tr
                        class="bg-white border-b dark:bg-gray-800 dark:border-gray-700"
                    >
                        <td class="px-6 py-4">{item.symbol}</td>
                        <td class="px-6 py-4">{item.price.toFixed()} USDT</td>
                        <td class="px-6 py-4">{item.amount} </td>
                        <td class="px-6 py-4">{item.value.toFixed()} USDT</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</main>
