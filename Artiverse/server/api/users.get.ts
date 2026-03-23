import type { User } from '@/types/user'

export default defineEventHandler(() => {
  const users = [
    { id: 1, name: 'nico_dev', email: 'nico.dev@example.com', avatar: 'https://i.pravatar.cc/150?img=12', isActive: true, age: 28},
    { id: 2, name: 'alice_ui', email: 'alice.ui@example.com', avatar: 'https://i.pravatar.cc/150?img=32', isActive: false, age: 26},
    { id: 3, name: 'bob_ts', email: 'bob.ts@example.com', avatar: 'https://i.pravatar.cc/150?img=56', isActive: true, age: 31,},
    { id: 4, name: 'clara_nuxt', email: 'clara.nuxt@example.com', avatar: 'https://i.pravatar.cc/150?img=68', isActive: false, age: 29},
    { id: 5, name: 'julien_js', email: 'julien.js@example.com', avatar: 'https://i.pravatar.cc/150?img=5', isActive: true, age: 27},
    { id: 6, name: 'emma_css', email: 'emma.css@example.com', avatar: 'https://i.pravatar.cc/150?img=6', isActive: true, age: 24},
    { id: 7, name: 'thomas_node', email: 'thomas.node@example.com', avatar: 'https://i.pravatar.cc/150?img=7', isActive: false, age: 33},
    { id: 8, name: 'lea_vue', email: 'lea.vue@example.com', avatar: 'https://i.pravatar.cc/150?img=8', isActive: true, age: 25},
    { id: 9, name: 'max_react', email: 'max.react@example.com', avatar: 'https://i.pravatar.cc/150?img=9', isActive: true, age: 30},
    { id: 10, name: 'sarah_api', email: 'sarah.api@example.com', avatar: 'https://i.pravatar.cc/150?img=10', isActive: false, age: 32,},
    { id: 11, name: 'kevin_sql', email: 'kevin.sql@example.com', avatar: 'https://i.pravatar.cc/150?img=11', isActive: true, age: 35},
    { id: 12, name: 'lucas_php', email: 'lucas.php@example.com', avatar: 'https://i.pravatar.cc/150?img=13', isActive: false, age: 29},
    { id: 13, name: 'manon_git', email: 'manon.git@example.com', avatar: 'https://i.pravatar.cc/150?img=14', isActive: true, age: 26},
    { id: 14, name: 'paul_docker', email: 'paul.docker@example.com', avatar: 'https://i.pravatar.cc/150?img=15', isActive: true, age: 34},
    { id: 15, name: 'ines_test', email: 'ines.test@example.com', avatar: 'https://i.pravatar.cc/150?img=16', isActive: false, age: 27},
    { id: 16, name: 'hugo_ci', email: 'hugo.ci@example.com', avatar: 'https://i.pravatar.cc/150?img=17', isActive: true, age: 28},
    { id: 17, name: 'camille_ux', email: 'camille.ux@example.com', avatar: 'https://i.pravatar.cc/150?img=18', isActive: false, age: 25},
    { id: 18, name: 'antoine_algo', email: 'antoine.algo@example.com', avatar: 'https://i.pravatar.cc/150?img=19', isActive: true, age: 36},
    { id: 19, name: 'jade_mobile', email: 'jade.mobile@example.com', avatar: 'https://i.pravatar.cc/150?img=20', isActive: true, age: 28},
    { id: 20, name: 'romain_flutter', email: 'romain.flutter@example.com', avatar: 'https://i.pravatar.cc/150?img=21', isActive: false, age: 30},
    { id: 21, name: 'lina_kotlin', email: 'lina.kotlin@example.com', avatar: 'https://i.pravatar.cc/150?img=22', isActive: true, age: 27},
    { id: 22, name: 'yann_swift', email: 'yann.swift@example.com', avatar: 'https://i.pravatar.cc/150?img=23', isActive: false, age: 31},
    { id: 23, name: 'nora_graphql', email: 'nora.graphql@example.com', avatar: 'https://i.pravatar.cc/150?img=24', isActive: true, age: 29},
    { id: 24, name: 'quentin_rest', email: 'quentin.rest@example.com', avatar: 'https://i.pravatar.cc/150?img=25', isActive: true, age: 32},
    { id: 25, name: 'zoe_auth', email: 'zoe.auth@example.com', avatar: 'https://i.pravatar.cc/150?img=26', isActive: false, age: 28},
    { id: 26, name: 'axel_oauth', email: 'axel.oauth@example.com', avatar: 'https://i.pravatar.cc/150?img=27', isActive: true, age: 33},
    { id: 27, name: 'marine_cache', email: 'marine.cache@example.com', avatar: 'https://i.pravatar.cc/150?img=28', isActive: false, age: 26},
    { id: 28, name: 'benjamin_perf', email: 'benjamin.perf@example.com', avatar: 'https://i.pravatar.cc/150?img=29', isActive: true, age: 34},
    { id: 29, name: 'eva_cloud', email: 'eva.cloud@example.com', avatar: 'https://i.pravatar.cc/150?img=30', isActive: true, age: 30},
    { id: 30, name: 'leo_aws', email: 'leo.aws@example.com', avatar: 'https://i.pravatar.cc/150?img=31', isActive: false, age: 35},
    { id: 31, name: 'anais_azure', email: 'anais.azure@example.com', avatar: 'https://i.pravatar.cc/150?img=33', isActive: true, age: 29},
    { id: 32, name: 'sam_gcp', email: 'sam.gcp@example.com', avatar: 'https://i.pravatar.cc/150?img=34', isActive: true, age: 31},
    { id: 33, name: 'elise_logs', email: 'elise.logs@example.com', avatar: 'https://i.pravatar.cc/150?img=35', isActive: false, age: 27},
    { id: 34, name: 'victor_sec', email: 'victor.sec@example.com', avatar: 'https://i.pravatar.cc/150?img=36', isActive: true, age: 37},
    { id: 35, name: 'pauline_rgpd', email: 'pauline.rgpd@example.com', avatar: 'https://i.pravatar.cc/150?img=37', isActive: false, age: 32},
    { id: 36, name: 'noah_encrypt', email: 'noah.encrypt@example.com', avatar: 'https://i.pravatar.cc/150?img=38', isActive: true, age: 28},
    { id: 37, name: 'cloe_backup', email: 'cloe.backup@example.com', avatar: 'https://i.pravatar.cc/150?img=39', isActive: true, age: 26},
    { id: 38, name: 'mathis_k8s', email: 'mathis.k8s@example.com', avatar: 'https://i.pravatar.cc/150?img=40', isActive: false, age: 33},
    { id: 39, name: 'iris_monitor', email: 'iris.monitor@example.com', avatar: 'https://i.pravatar.cc/150?img=41', isActive: true, age: 29},
    { id: 40, name: 'adam_event', email: 'adam.event@example.com', avatar: 'https://i.pravatar.cc/150?img=42', isActive: false, age: 30},
    { id: 41, name: 'sofia_queue', email: 'sofia.queue@example.com', avatar: 'https://i.pravatar.cc/150?img=43', isActive: true, age: 27},
    { id: 42, name: 'nathan_realtime', email: 'nathan.realtime@example.com', avatar: 'https://i.pravatar.cc/150?img=44', isActive: true, age: 31}
  ].map((user) => ({
    ...user,
    role: user.id % 10 === 0 ? 'admin' : 'user'
  })) as User[]

  return users;
})
