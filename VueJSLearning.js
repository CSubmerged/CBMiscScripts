// Vue.component('todo-item', {
//     template: `
//     <li>
//       {{ title }}
//       <button v-on:click="$emit(\'remove\')">Remove</button>
//     </li>
//   `,
//     props: ['title']
// });
//
// new Vue({
//     el: '#todo-list-example',
//     data: {
//         newTodoText: '',
//         todos: [
//             {
//                 id: 1,
//                 title: 'Do the dishes',
//             },
//             {
//                 id: 2,
//                 title: 'Take out the trash',
//             },
//             {
//                 id: 3,
//                 title: 'Mow the lawn'
//             }
//         ],
//         nextTodoId: 4
//     },
//     methods: {
//         addNewTodo: function () {
//             this.todos.push({
//                 id: this.nextTodoId++,
//                 title: this.newTodoText
//             });
//             this.newTodoText = ''
//         }
//     },
//     delimiters: ['<%', '%>']
// });


Vue.component('counter', {
    template: '<div class="box box-info">\
                   <div class="box-title"><strong><h3> Counter </h3></strong></div>\
                   <div class="box-body">\
                   <h3>{{ currNo }}</h3>\
                   <button v-on:click="currNoReset">Reset</button>\
                   <button v-on:click="currNoDec">-</button>\
                   <button v-on:click="currNoInc">+</button>\
                   <p>Step by <input v-model.number="step" type="number"></p>\
                   </div>\
                   </div>',
    data: function () {
        return {currNo: 0, step: 1};},
    methods: {
        currNoInc: function () {
            this.currNo += this.step;
        },
        currNoDec: function () {
            this.currNo -= this.step;
        },
        currNoReset: function () {
            this.currNo = 0;
            this.step = 1;
        }
    }
});
new Vue({
    el: '#counter-example',
    data: {
        sliderValue: 1,
        counters: [{
            id: 1,
            currNo: 0,
            step: 1
        }]
    },
    methods: {
        changeSlider: function () {
            this.instances = this.sliderValue;
        }
    },
    template: `<div>
<div class="slidecontainer">
                <input type="range" min="1" max="20" v-model.number="sliderValue" @input="changeSlider" class="slider" id="myRange" width="20">
            </div>
            Number of Counters: {{ sliderValue }}

            <counter
                    v-for="i in sliderValue"
                    v-bind:key="i"
                    />
                    

</div>`
});

// ----------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------


// HTML
{#    <div id="todo-list-example">#}
{#        <form v-on:submit.prevent="addNewTodo">#}
{#            <label for="new-todo">Add a todo</label>#}
{#            <input#}
{#                    v-model="newTodoText"#}
{#                    id="new-todo"#}
{#                    placeholder="E.g. Feed the cat"#}
{#            >#}
{#            <button>Add</button>#}
{#        </form>#}
{#        <ul>#}
{#            <li#}
{#                    is="todo-item"#}
{#                    v-for="(todo, index) in todos"#}
{#                    v-bind:key="todo.id"#}
{#                    v-bind:title="todo.title"#}
{#                    v-on:remove="todos.splice(index, 1)"#}
{#            ></li>#}
{#        </ul>#}
{#    </div>#}
{##}
{#    <script src="{{ static_url('js/vue-components/profile.js') }}"></script>#}

    {#    -------------------------------------------------------------#}


    <div>
        <div id="counter-example">
        </div>
    </div>

    <script src="{{ static_url('js/vue-components/profile.js') }}"></script>



{#    <script>#}
{#    Vue.component('counter', {#}
{#        template: '<div class="box box-info">\#}
{#                   <div class="box-title"><strong><h3> Counter </h3></strong></div>\#}
{#                   <div class="box-body">\#}
{#                   <h3><% currNo %></h3>\#}
{#                   <button v-on:click="currNoReset">Reset</button>\#}
{#                   <button v-on:click="currNoDec">-</button>\#}
{#                   <button v-on:click="currNoInc">+</button>\#}
{#                   <p>Step by <input v-model.number="step" type="number"></p>\#}
{#                   </div>\#}
{#                   </div>',#}
{#        props: ['currNo', 'step']#}
{#    });#}
{#        new Vue({#}
{#            el: '#counter-example',#}
{#            data: {#}
{#                sliderValue: 1,#}
{#                instances: 1,#}
{#                counters: {#}
{#                    id: 1,#}
{#                    currNo: 0,#}
{#                    step: 1,#}
{#                }#}
{#            },#}
{#            delimiters: ['<%', '%>'],#}
{#            methods: {#}
{#                currNoInc: function () {#}
{#                    this.currNo += this.step;#}
{#                },#}
{#                currNoDec: function () {#}
{#                    this.currNo -= this.step;#}
{#                },#}
{#                currNoReset: function () {#}
{#                    this.currNo = 0;#}
{#                },#}
{#                changeSlider: function () {#}
{#                    this.instances = this.sliderValue;#}
{#                }#}
{#            }#}
{#        });#}
{#    </script>#}

{#    -------------------------------------------------------------#}

{#<div class="row">#}
{#    <div class="col-md-3">#}
{#        <div class="box box-primary">#}
{#            <div class="box-body box-profile">#}
{#                <img class="profile-user-img img-responsive img-circle" src="{{ current_user.avatar }}" alt="No User Profile Picture Found">#}
{#                <h3 class="profile-username text-center">{{ current_user.name }}</h3>#}
{#                {% for role in current_user.roles %}#}
{#                    <p class="text-muted text-center">{{ role }}</p>#}
{#                {% endfor %}#}
{#            </div>#}
{#        </div>#}
{#    </div>#}
{#    <div class="col-md-9">#}
{#        <div class="nav-tabs-custom">#}
{#            <ul class="nav nav-tabs">#}
{#                <li class="active">#}
{#                    <a href="#settings" data-toggle="tab" aria-expanded="true">Settings</a>#}
{#                </li>#}
{#                <li class>#}
{#                    <a href="#vuetest" data-toggle="tab" aria-expanded="false">VueTest</a>#}
{#                </li>#}
{#            </ul>#}
{#            <div class="tab-content">#}
{#                <div class="tab-pane active" id="settings">#}
{#                    <h3>Look at all those Chickens</h3>#}
{#                    <img src="https://i.imgflip.com/1n6nnu.jpg">#}
{#                </div>#}
{#                <div class="tab-pane" id="vuetest">#}
{#                    <h3>Here come Dat Boi</h3>#}
{#                    <img src="http://images.adagio.com/images2/custom_blends/120105.jpg">#}
{#                </div>#}
{#            </div>#}
{#        </div>#}
{#    </div>#}
{#</div>#}