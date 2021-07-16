let dom1 = document.getElementById("net1");
let myChart1 = echarts.init(dom1);
myChart1.showLoading();

let dom2 = document.getElementById("net2");
let myChart2 = echarts.init(dom2);
myChart2.showLoading();

$.get('../static/data/academia.gexf', function (xml) {
    myChart1.hideLoading();
    myChart2.hideLoading();

    var graph = echarts.dataTool.gexf.parse(xml);
    var categories = [];
    for (let i = 0; i < 14; i++) {
        categories[i] = {
            name: 'Class' + i
        };
    }
    graph.nodes.forEach(function (node) {
        node.itemStyle = null;
        node.value = node.symbolSize;
        node.symbolSize /= 2;
        node.label = {
            show: node.symbolSize > 11
        };
        node.category = node.attributes.modularity_class;
    });
    let color = [
            "#2ec7c9",
            "#b6a2de",
            "#5ab1ef",
            "#ffb980",
            "#8d98b3",
            "#e5cf0d",
            "#97b552",
            "#07a2a4",
            "#9a7fd1",
            "#588dd5",
            "#f5994e",
            ];
    let option1 = {
        title: {},
        tooltip: {},
        color: color,
        legend: [{
            // selectedMode: 'single',
            data: categories.map(function (a) {
                return a.name;
            }),
            show: false,
        }],
        animationDuration: 5000,
        animationEasingUpdate: 'quinticInOut',
        series : [
            {
                name: 'Academia Network',
                type: 'graph',
                layout: 'none',
                data: graph.nodes,
                links: graph.links,
                categories: categories,
                roam: true,
                zoom: 1.2,
                focusNodeAdjacency: true,
                itemStyle: {
                    borderColor: '#fff',
                    borderWidth: 1,
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.3)'
                },
                label: {
                    position: 'right',
                    formatter: '{b}'
                },
                lineStyle: {
                    color: 'source',
                    curveness: 0.3
                },
                emphasis: {
                    lineStyle: {
                        width: 5
                    }
                }
            }
        ]
    };

    let option2 = {
        title: {},
        tooltip: {},
        color: color,
        legend: [{
            // selectedMode: 'single',
            data: categories.map(function (a) {
                return a.name;
            }),
            show: false,
        }],
        animationDuration: 5000,
        animationEasingUpdate: 'quinticInOut',
        series: [
            {
                name: 'Academia Network',
                type: 'graph',
                layout: 'circular',
                data: graph.nodes,
                links: graph.links,
                categories: categories,
                roam: true,
                zoom: 1.2,
                focusNodeAdjacency: true,
                itemStyle: {
                    borderColor: '#fff',
                    borderWidth: 1,
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.3)'
                },
                label: {
                    formatter: '{b}'
                },
                lineStyle: {
                    color: 'source',
                    curveness: 0.3
                },
                emphasis: {
                    lineStyle: {
                        width: 5
                    }
                }
            }
        ]
    };

    myChart1.setOption(option1);
    myChart2.setOption(option2);
}, 'xml');

